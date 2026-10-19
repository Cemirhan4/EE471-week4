from flask import Flask, request, jsonify, render_template
from custom_classes import (
    Book, DVD, LibraryCollection,
    ItemNotFoundError, ItemStateError
)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# --- One shared LibraryCollection instance, seeded with mixed items ---
library = LibraryCollection()
library.add_item(Book("The Great Gatsby", "F. Scott Fitzgerald", page_count=180))
library.add_item(DVD("Inception", "Christopher Nolan", duration=148))
library.add_item(Book("1984", "George Orwell", page_count=328))
library.add_item(DVD("Arrival", "Denis Villeneuve", duration=116))
library.add_item(Book("The Hobbit", "J.R.R. Tolkien", page_count=310))


# --- Helper ---
def error(message, status=400):
    return jsonify({"error": message}), status


# --- POST /api/items — Create a Book or DVD ---
@app.route('/api/items', methods=['POST'])
def create_item():
    data = request.get_json()
    if not data:
        return error("Invalid JSON input.")

    item_type = data.get('type', '').lower()
    title = data.get('title')
    author = data.get('author')

    if not title or not author or not item_type:
        return error("Fields 'type', 'title', and 'author' are required.")

    if item_type == 'book':
        page_count = data.get('page_count')
        if page_count is None:
            return error("Field 'page_count' is required for books.")
        try:
            page_count = int(page_count)
        except (ValueError, TypeError):
            return error("'page_count' must be an integer.")
        item = Book(title, author, page_count)

    elif item_type == 'dvd':
        duration = data.get('duration')
        if duration is None:
            return error("Field 'duration' is required for DVDs.")
        try:
            duration = int(duration)
        except (ValueError, TypeError):
            return error("'duration' must be an integer.")
        item = DVD(title, author, duration)

    else:
        return error("'type' must be 'book' or 'dvd'.")

    assigned_id = library.add_item(item)
    return jsonify(library.get_item(assigned_id).to_dict()), 201


# --- GET /api/items — List items with optional filters ---
@app.route('/api/items', methods=['GET'])
def list_items():
    available_param = request.args.get('available')
    type_param = request.args.get('type')

    # Parse available filter
    available = None
    if available_param is not None:
        if available_param.lower() == 'true':
            available = True
        elif available_param.lower() == 'false':
            available = False
        else:
            return error("'available' filter must be 'true' or 'false'.")

    # Parse type filter
    item_type = None
    if type_param is not None:
        if type_param.lower() == 'book':
            item_type = Book
        elif type_param.lower() == 'dvd':
            item_type = DVD
        else:
            return error("'type' filter must be 'book' or 'dvd'.")

    items = library.list_items(available=available, item_type=item_type)
    return jsonify([item.to_dict() for item in items]), 200


# --- GET /api/items/<id> — Get one item ---
@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    try:
        item = library.get_item(item_id)
        return jsonify(item.to_dict()), 200
    except ItemNotFoundError as e:
        return error(str(e), 404)


# --- PUT /api/items/<id> — Replace all editable fields ---
@app.route('/api/items/<int:item_id>', methods=['PUT'])
def replace_item(item_id):
    data = request.get_json()
    if not data:
        return error("Invalid JSON input.")

    try:
        item = library.get_item(item_id)
    except ItemNotFoundError as e:
        return error(str(e), 404)

    title = data.get('title')
    author = data.get('author')

    if not title or not author:
        return error("Fields 'title' and 'author' are required.")

    fields = {"title": title, "author": author}

    if isinstance(item, Book):
        page_count = data.get('page_count')
        if page_count is None:
            return error("Field 'page_count' is required for books.")
        try:
            fields['page_count'] = int(page_count)
        except (ValueError, TypeError):
            return error("'page_count' must be an integer.")

    elif isinstance(item, DVD):
        duration = data.get('duration')
        if duration is None:
            return error("Field 'duration' is required for DVDs.")
        try:
            fields['duration'] = int(duration)
        except (ValueError, TypeError):
            return error("'duration' must be an integer.")

    try:
        library.update_item(item_id, **fields)
        return jsonify(library.get_item(item_id).to_dict()), 200
    except ValueError as e:
        return error(str(e))


# --- PATCH /api/items/<id> — Update some editable fields ---
@app.route('/api/items/<int:item_id>', methods=['PATCH'])
def update_item(item_id):
    data = request.get_json()
    if not data:
        return error("Invalid JSON input.")

    try:
        library.get_item(item_id)
    except ItemNotFoundError as e:
        return error(str(e), 404)

    # Convert page_count and duration to int if present
    if 'page_count' in data:
        try:
            data['page_count'] = int(data['page_count'])
        except (ValueError, TypeError):
            return error("'page_count' must be an integer.")

    if 'duration' in data:
        try:
            data['duration'] = int(data['duration'])
        except (ValueError, TypeError):
            return error("'duration' must be an integer.")

    try:
        library.update_item(item_id, **data)
        return jsonify(library.get_item(item_id).to_dict()), 200
    except ValueError as e:
        return error(str(e))


# --- DELETE /api/items/<id> — Remove an item ---
@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    try:
        library.remove_item(item_id)
        return '', 204
    except ItemNotFoundError as e:
        return error(str(e), 404)
    except ItemStateError as e:
        return error(str(e), 409)


# --- POST /api/items/<id>/checkout — Check out an item ---
@app.route('/api/items/<int:item_id>/checkout', methods=['POST'])
def checkout_item(item_id):
    try:
        item = library.get_item(item_id)
        message = item.checkout()
        return jsonify({"message": message, "item": item.to_dict()}), 200
    except ItemNotFoundError as e:
        return error(str(e), 404)
    except ItemStateError as e:
        return error(str(e), 409)


# --- POST /api/items/<id>/return — Return an item ---
@app.route('/api/items/<int:item_id>/return', methods=['POST'])
def return_item(item_id):
    try:
        item = library.get_item(item_id)
        item.return_item()
        return jsonify({"message": "Item returned successfully.", "item": item.to_dict()}), 200
    except ItemNotFoundError as e:
        return error(str(e), 404)
    except ItemStateError as e:
        return error(str(e), 409)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
