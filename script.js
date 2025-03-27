
let promptCount = 5;

function createPromptBox(index) {
    const div = document.createElement('div');
    div.innerHTML = `<label for="prompt${index}">Prompt ${index}</label><textarea id="prompt${index}" name="prompt${index}" rows="4"></textarea>`;
    return div;
}

function updatePromptBoxes() {
    const container = document.getElementById('prompt-boxes');
    container.innerHTML = '';
    for (let i = 1; i <= promptCount; i++) {
        container.appendChild(createPromptBox(i));
    }
}

document.getElementById('add-prompt').addEventListener('click', () => {
    promptCount++;
    updatePromptBoxes();
});

document.getElementById('prompt-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const prompts = [];
    for (let i = 1; i <= promptCount; i++) {
        prompts.push(document.getElementById(`prompt${i}`).value);
    }

    const response = await fetch('/run', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ prompts })
    });
    const result = await response.json();
    document.getElementById('result-text').textContent = result.output;
});

updatePromptBoxes();
