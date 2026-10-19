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

## Corrections Made
- Changed operator mapping to support ÷ and × symbols correctly
- Added reset state after equals is pressed
- Fixed display not clearing when starting a new number after result
