document.addEventListener('DOMContentLoaded', () => {
  const links = document.querySelectorAll('a');
  links.forEach(link => {
    link.addEventListener('click', (e) => {
      if (link.getAttribute('href').endsWith('.py')) {
        e.preventDefault();
        fetch(link.getAttribute('href'))
          .then(response => response.text())
          .then(code => {
            alert(`Code content:\n\n${code}`);
          })
          .catch(error => {
            console.error('Error fetching code:', error);
          });
      }
    });
  });
});
