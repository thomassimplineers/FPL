// Hantera klick på nedladdningsknappen
document.getElementById('download-button').addEventListener('click', () => {
  window.location.href = 'https://fpl-analyzer-backend.herokuapp.com/download_excel';
});

// Hantera GPT-frågor
document.getElementById('ask-button').addEventListener('click', async () => {
  const question = document.getElementById('question-input').value;
  const answer = await askGPT(question);
  document.getElementById('answer-output').innerText = answer;
});

async function askGPT(question) {
  const response = await fetch('https://fpl-analyzer-backend.herokuapp.com/ask_gpt', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ question: question })
  });
  const data = await response.json();
  return data.answer;
}
