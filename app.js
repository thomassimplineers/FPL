// Hantera klick på nedladdningsknappen
document.getElementById('download-button').addEventListener('click', () => {
  window.location.href = 'https://fpl-analyzer-backend.herokuapp.com/download_excel';
});
