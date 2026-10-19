# --- Custom Exceptions ---

class ItemNotFoundError(Exception):
    """Raised when an item with the given ID does not exist in the collection."""
    pass


class ItemStateError(Exception):
    """Raised when a checkout or return action is invalid given the item's current state."""
    pass


# --- Base Class ---

class MediaItem:
    """
    Represents a generic item in a library collection.

    This is the base class for all media types. It provides
    core checkout and return functionality shared by all items.
    """

    def __init__(self, title, author, is_available=True):
        """
        Initialize a MediaItem.

        Args:
            title (str): The title of the media item.
            author (str): The author or creator of the item.
            is_available (bool): Whether the item is available for checkout. Defaults to True.
        """
        self.id = None  # Assigned by LibraryCollection.add_item()
        self.title = title
        self.author = author
        self.is_available = is_available

    def checkout(self):
        """
        Check out the item if it is currently available.

        Returns:
            str: 'Successful checkout' if available.

        Raises:
            ItemStateError: If the item is already checked out.
        """
        if self.is_available:
            self.is_available = False
            return "Successful checkout"
        else:
            raise ItemStateError(f"'{self.title}' is already checked out.")

    def return_item(self):
        """
        Mark the item as available again after being returned.

        Raises:
            ItemStateError: If the item is not currently checked out.
        """
        if self.is_available:
            raise ItemStateError(f"'{self.title}' is not currently checked out.")
        self.is_available = True

    def to_dict(self):
        """
        Return a dictionary representation of the item.

        Returns:
            dict: Contains id, type, title, author, is_available.
        """
        return {
            "id": self.id,
            "type": type(self).__name__,
            "title": self.title,
            "author": self.author,
            "is_available": self.is_available,
        }

    def __str__(self):
        """Return a human-readable string representation of the item."""
        status = "Available" if self.is_available else "Checked Out"
        return f"{self.title} by {self.author} [{status}]"


# --- Subclasses ---

class Book(MediaItem):
    """
    Represents a book in the library.

    Extends MediaItem with a page count attribute and
    includes page count in its string representation.
    """

    def __init__(self, title, author, page_count, is_available=True):
        """
        Initialize a Book.

        Args:
            title (str): The title of the book.
            author (str): The author of the book.
            page_count (int): Total number of pages.
            is_available (bool): Availability status. Defaults to True.
        """
        super().__init__(title, author, is_available)
        self.page_count = page_count

    def to_dict(self):
        """Return a dictionary representation including page_count."""
        data = super().to_dict()
        data["page_count"] = self.page_count
        return data

    def __str__(self):
        """Return a string representation that includes the page count."""
        status = "Available" if self.is_available else "Checked Out"
        return f"{self.title} by {self.author} [{status}] - {self.page_count} pages"


class DVD(MediaItem):
    """
    Represents a DVD in the library.

    Extends MediaItem with a duration attribute. DVDs are fragile,
    so a care reminder is returned (not printed) on every successful checkout.
    """

    def __init__(self, title, author, duration, is_available=True):
        """
        Initialize a DVD.

        Args:
            title (str): The title of the DVD.
            author (str): The director or creator.
            duration (int): Duration of the DVD in minutes.
            is_available (bool): Availability status. Defaults to True.
        """
        super().__init__(title, author, is_available)
        self.duration = duration

    def checkout(self):
        """
        Check out the DVD, returning a care reminder on success.

        Returns:
            str: Success message with fragility reminder if available.

        Raises:
            ItemStateError: If the DVD is already checked out.
        """
        result = super().checkout()
        # DVDs can be scratched easily — reminder is returned, not printed
        return f"{result} — Handle with care: Do not scratch the disc."

    def to_dict(self):
        """Return a dictionary representation including duration."""
        data = super().to_dict()
        data["duration"] = self.duration
        return data

    def __str__(self):
        """Return a string representation that includes the duration."""
        status = "Available" if self.is_available else "Checked Out"
        return f"{self.title} by {self.author} [{status}] - {self.duration} mins"


# --- Collection ---

class LibraryCollection:
    """
    A container for managing a collection of MediaItems.

    Supports adding, retrieving, updating, removing, and listing items.
    IDs are auto-incremented and never reused after deletion.
    """

    def __init__(self):
        """Initialize the collection with an empty list and ID counter."""
        self.items = []
        self._next_id = 1

    def add_item(self, item):
        """
        Add a MediaItem to the collection and assign it a unique ID.

        Args:
            item (MediaItem): The item to add.

        Returns:
            int: The assigned unique ID of the item.
        """
        item.id = self._next_id
        self._next_id += 1
        self.items.append(item)
        return item.id

    def get_item(self, item_id):
        """
        Retrieve an item by its ID.

        Args:
            item_id (int): The ID of the item to retrieve.

        Returns:
            MediaItem: The item with the given ID.

        Raises:
            ItemNotFoundError: If no item with the given ID exists.
        """
        for item in self.items:
            if item.id == item_id:
                return item
        raise ItemNotFoundError(f"No item found with ID {item_id}.")

    def list_items(self, available=None, item_type=None):
        """
        Return all items, optionally filtered by availability and/or type.

        Args:
            available (bool or None): If True, return only available items.
                                      If False, return only checked-out items.
                                      If None, return all items.
            item_type (type or None): Filter by class type (e.g. Book, DVD).

        Returns:
            list[MediaItem]: Filtered list of items.
        """
        result = self.items
        if available is not None:
            result = [i for i in result if i.is_available == available]
        if item_type is not None:
            result = [i for i in result if isinstance(i, item_type)]
        return result

    def update_item(self, item_id, **fields):
        """
        Update editable fields of an item.

        Editable fields: title, author, page_count, duration.
        Attempting to change id, type, or is_available raises ValueError.

        Args:
            item_id (int): The ID of the item to update.
            **fields: Key-value pairs of fields to update.

        Raises:
            ItemNotFoundError: If no item with the given ID exists.
            ValueError: If attempting to modify a non-editable field.
        """
        item = self.get_item(item_id)
        forbidden = {"id", "type", "is_available"}
        for key in fields:
            if key in forbidden:
                raise ValueError(f"Cannot update field '{key}' — it is not editable.")
        for key, value in fields.items():
            setattr(item, key, value)

    def remove_item(self, item_id):
        """
        Remove an item from the collection by its ID.

        Args:
            item_id (int): The ID of the item to remove.

        Raises:
            ItemNotFoundError: If no item with the given ID exists.
            ItemStateError: If the item is currently checked out.
        """
        item = self.get_item(item_id)
        if not item.is_available:
            raise ItemStateError(f"Cannot remove '{item.title}' — it is currently checked out.")
        self.items.remove(item)

    def list_available(self):
        """
        Return the titles of all currently available items.

        Returns:
            list[str]: A list of available item titles.
        """
        return [item.title for item in self.items if item.is_available]