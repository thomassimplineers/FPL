// Hantera klick på nedladdningsknappen
document.getElementById('download-button').addEventListener('click', () => {
  window.location.href = 'https://fpl-analyzer-backend.herokuapp.com/download_excel';
});

// Hantera GPT-frågor
document.getElementById('ask-button').addEventListener('click', async () => {
  const question = document.getElementById('question-input').value;
  try {
    const answer = await askGPT(question);
    document.getElementById('answer-output').innerText = answer;
  } catch (error) {
    document.getElementById('answer-output').innerText = 'Ett fel uppstod: ' + error.message;
    console.error('Fel vid GPT-anropet:', error);
  }
});

async function askGPT(question) {
  const response = await fetch('https://fpl-analyzer-backend.herokuapp.com/ask_gpt', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'my_secure_key_12345'  // Lägg till din BACKEND_API_KEY här
    },
    body: JSON.stringify({ question: question })
  });

  // Hantera svar och fel
  if (!response.ok) {
    console.error('Fel vid GPT-anropet:', await response.json());
    return 'Ett fel uppstod vid anropet till GPT.';
  }

  const data = await response.json();
  return data.answer;
}

    const data = await response.json();
    return data.answer;
  } catch (error) {
    console.error('Fel vid hämtning:', error);
    throw error;
  }
}
