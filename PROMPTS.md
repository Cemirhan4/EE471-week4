# PROMPTS.md — AI Prompts Log

## Tool Used
**Antigravity (AI Coding Assistant)**

---

## Section 1 – Part 2 Prompts

### Prompt 1
> "Build a Flask backend with a POST /api/calculate endpoint that takes num1, operator, and num2 as JSON and returns the result. No eval(). Handle division by zero and invalid inputs."

### Prompt 2
> "Create an HTML/CSS/JS calculator that matches my Figma design — dark background, circular buttons, blue operators, and connects to the Flask /api/calculate API."

### Prompt 3
> "Make sure the display shows the result from the Flask server, not calculated in the browser."

---

## Corrections Made (Section 1)
- Changed operator mapping to support ÷ and × symbols correctly
- Added reset state after equals is pressed
- Fixed display not clearing when starting a new number after result

---

## Section 2 – Part 4 Prompts (Library Web App)

### Prompt 1
> "Convert the Figma library catalog design into HTML (templates/index.html) and CSS (static/style.css). It should have an editorial look with serif headings, a warm cream background, an 'Add an item' form on the left, and a catalog cards list on the right with filter tabs and an available toggle."

### Prompt 2
> "Write script.js to connect the frontend to the Flask REST API at /api/items. Support GET with query filters, POST for creating items, PUT for editing, DELETE for removing items, and POST for checkout and return."

### Prompt 3
> "Make sure that API errors, especially 409 Conflict when attempting to delete a checked-out item or checking out an already checked-out item, are prominently displayed in an error notification area."

---

## Corrections Made (Section 2)
1. **Error Status Code Handling & Display:**
   - *Issue:* The initial AI-generated JavaScript only showed a generic alert() for failed requests and did not parse the JSON error body (`{"error": "<message>"}`) from the server.
   - *Fix:* Replaced generic handling with a dedicated `#notification-area` error banner that extracts `data.error` and displays the exact 409 / 404 / 400 error messages returned by `custom_classes.py` through Flask.

2. **Eliminated Duplicated Business Logic in JavaScript:**
   - *Issue:* The initial code attempted to duplicate business rules in JavaScript (e.g. blocking delete clicks locally if `item.is_available === false`).
   - *Fix:* Removed client-side rule duplication so all business logic stays strictly inside `custom_classes.py` as required by the assignment. The frontend now sends the DELETE/checkout/return request directly to the API and relies on the backend to enforce `ItemStateError` and return HTTP 409.

3. **Dynamic Form Fields for Book vs. DVD:**
   - *Issue:* The form initially displayed both `page_count` and `duration` simultaneously, causing confusion and validation failures on the API.
   - *Fix:* Added dynamic toggling so selecting "Book" displays "Page count" (pages), while selecting "DVD" displays "Duration" (mins), correctly mapping to the respective Python class constructor.
