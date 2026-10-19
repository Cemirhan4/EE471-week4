from custom_classes import (
    MediaItem, Book, DVD, LibraryCollection,
    ItemNotFoundError, ItemStateError
)

library = LibraryCollection()

print("=" * 50)
print("=== Adding Items ===")
print("=" * 50)

id1 = library.add_item(Book("The Hobbit", "J.R.R. Tolkien", page_count=310))
id2 = library.add_item(DVD("Interstellar", "Christopher Nolan", duration=169))
id3 = library.add_item(Book("1984", "George Orwell", page_count=328))
id4 = library.add_item(DVD("The Matrix", "Wachowski Sisters", duration=136))

print(f"Added Book ID: {id1}")
print(f"Added DVD  ID: {id2}")
print(f"Added Book ID: {id3}")
print(f"Added DVD  ID: {id4}")

# --- list_items ---
print("\n" + "=" * 50)
print("=== list_items() — All Items ===")
print("=" * 50)
for item in library.list_items():
    print(item.to_dict())

# --- get_item ---
print("\n" + "=" * 50)
print("=== get_item() ===")
print("=" * 50)
item = library.get_item(id1)
print(f"Found: {item}")

# --- get_item — ItemNotFoundError ---
print("\nTrying to get item with invalid ID (999)...")
try:
    library.get_item(999)
except ItemNotFoundError as e:
    print(f"ItemNotFoundError caught: {e}")

# --- checkout ---
print("\n" + "=" * 50)
print("=== checkout() ===")
print("=" * 50)
print(f"Checking out '{library.get_item(id1).title}'...")
print(library.get_item(id1).checkout())

print(f"\nChecking out DVD '{library.get_item(id2).title}'...")
print(library.get_item(id2).checkout())

# --- checkout — ItemStateError ---
print("\nTrying to check out already-checked-out item...")
try:
    library.get_item(id1).checkout()
except ItemStateError as e:
    print(f"ItemStateError caught: {e}")

# --- return_item ---
print("\n" + "=" * 50)
print("=== return_item() ===")
print("=" * 50)
print(f"Returning '{library.get_item(id1).title}'...")
library.get_item(id1).return_item()
print(f"Is available: {library.get_item(id1).is_available}")

# --- return_item — ItemStateError ---
print("\nTrying to return an item that is not checked out...")
try:
    library.get_item(id1).return_item()
except ItemStateError as e:
    print(f"ItemStateError caught: {e}")

# --- list_items filtered ---
print("\n" + "=" * 50)
print("=== list_items(available=True) ===")
print("=" * 50)
for item in library.list_items(available=True):
    print(item)

print("\n=== list_items(item_type=Book) ===")
for item in library.list_items(item_type=Book):
    print(item)

print("\n=== list_items(available=False, item_type=DVD) ===")
for item in library.list_items(available=False, item_type=DVD):
    print(item)

# --- update_item ---
print("\n" + "=" * 50)
print("=== update_item() ===")
print("=" * 50)
print(f"Before update: {library.get_item(id3)}")
library.update_item(id3, title="Nineteen Eighty-Four", page_count=340)
print(f"After update:  {library.get_item(id3)}")

# --- update_item — ValueError ---
print("\nTrying to update a forbidden field (is_available)...")
try:
    library.update_item(id3, is_available=True)
except ValueError as e:
    print(f"ValueError caught: {e}")

# --- remove_item ---
print("\n" + "=" * 50)
print("=== remove_item() ===")
print("=" * 50)
print(f"Removing item ID {id3} ('{library.get_item(id3).title}')...")
library.remove_item(id3)
print(f"Items remaining: {len(library.items)}")

# --- remove_item — ItemStateError (checked out) ---
print("\nTrying to remove a checked-out item...")
try:
    library.remove_item(id2)  # id2 is still checked out
except ItemStateError as e:
    print(f"ItemStateError caught: {e}")

# --- remove_item — ItemNotFoundError ---
print("\nTrying to remove already-removed item...")
try:
    library.remove_item(id3)
except ItemNotFoundError as e:
    print(f"ItemNotFoundError caught: {e}")

# --- to_dict ---
print("\n" + "=" * 50)
print("=== to_dict() ===")
print("=" * 50)
print("Book to_dict:", library.get_item(id1).to_dict())
print("DVD  to_dict:", library.get_item(id2).to_dict())

print("\n" + "=" * 50)
print("=== All done! ===")
print("=" * 50)