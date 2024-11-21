// Hantera klick på nedladdningsknappen för analyserad spelardata
document.getElementById('download-analysis-button').addEventListener('click', () => {
    window.location.href = 'https://fpl-analyzer-backend.herokuapp.com/download_analysis';
});
