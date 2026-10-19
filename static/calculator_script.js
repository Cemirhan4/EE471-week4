let num1 = null;
let operator = null;
let waitingForNum2 = false;
const display = document.getElementById('display');

function updateDisplay(value) {
  display.textContent = value;
}

document.querySelectorAll('.btn').forEach(button => {
  button.addEventListener('click', () => {
    const val = button.dataset.val;

    if (button.classList.contains('num') && val !== '=') {
      handleNumber(val);
    } else if (button.classList.contains('op') && val !== '=') {
      handleOperator(val);
    } else if (val === '=') {
      handleEquals();
    }
  });
});

function handleNumber(val) {
  if (waitingForNum2) {
    updateDisplay(val);
    waitingForNum2 = false;
  } else {
    const current = display.textContent;
    if (val === '.' && current.includes('.')) return;
    updateDisplay(current === '0' ? val : current + val);
  }
}

function handleOperator(val) {
  num1 = parseFloat(display.textContent);
  operator = val;
  waitingForNum2 = true;
}

async function handleEquals() {
  if (num1 === null || operator === null) return;

  const num2 = parseFloat(display.textContent);

  // Map display symbols to API operators
  const opMap = { '÷': '÷', '×': 'x', '−': '-', '+': '+' };
  const apiOperator = opMap[operator] || operator;

  try {
    const response = await fetch('/api/calculate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ num1, operator: apiOperator, num2 })
    });

    const data = await response.json();

    if (data.error) {
      updateDisplay('Error');
      setTimeout(() => updateDisplay('0'), 1500);
    } else {
      updateDisplay(data.result);
    }
  } catch (err) {
    updateDisplay('Error');
    setTimeout(() => updateDisplay('0'), 1500);
  }

  // Reset state
  num1 = null;
  operator = null;
  waitingForNum2 = true;
}
