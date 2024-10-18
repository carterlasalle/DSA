document.addEventListener('DOMContentLoaded', () => {
  const folderStructureElement = document.getElementById('folder-structure');

  function createFolderElement(name, isRoot = false) {
    const folderElement = document.createElement('div');
    folderElement.classList.add('folder');
    if (isRoot) folderElement.classList.add('root');

    const folderNameElement = document.createElement('div');
    folderNameElement.classList.add('folder-name');
    folderNameElement.textContent = name;
    folderElement.appendChild(folderNameElement);

    const folderContentsElement = document.createElement('div');
    folderContentsElement.classList.add('folder-contents', 'hidden');
    folderElement.appendChild(folderContentsElement);

    folderNameElement.addEventListener('click', () => {
      folderContentsElement.classList.toggle('hidden');
      folderNameElement.classList.toggle('open');
    });

    return folderElement;
  }

  function createFileElement(name, path) {
    const fileElement = document.createElement('div');
    fileElement.classList.add('file');
    fileElement.textContent = name;
    fileElement.addEventListener('click', () => fetchFileContent(path));
    return fileElement;
  }

  function renderFolderStructure(structure, parentElement, currentPath = '') {
    for (const [name, content] of Object.entries(structure)) {
      const newPath = currentPath ? `${currentPath}/${name}` : name;
      if (content === null) {
        const fileElement = createFileElement(name, newPath);
        parentElement.appendChild(fileElement);
      } else {
        const folderElement = createFolderElement(name, parentElement === folderStructureElement);
        parentElement.appendChild(folderElement);
        renderFolderStructure(content, folderElement.querySelector('.folder-contents'), newPath);
      }
    }
  }

  function fetchFileContent(path) {
    const apiUrl = `https://api.github.com/repos/${GITHUB_USERNAME}/${REPO_NAME}/contents/${path}`;
    fetch(apiUrl)
      .then(response => response.json())
      .then(data => {
        const content = atob(data.content);
        alert(content);
      })
      .catch(error => console.error('Error fetching file content:', error));
  }

  function fetchFolderStructure() {
    fetch('structure.json', {
      headers: {
        'Content-Type': 'application/json',
        'Cache-Control': 'no-cache'
      }
    })
      .then(response => {
        if (!response.ok) {
          throw new Error('structure.json not found');
        }
        return response.text();
      })
      .then(text => {
        console.log('Raw response:', text);
        return JSON.parse(text);
      })
      .then(structure => {
        renderFolderStructure(structure, folderStructureElement);
      })
      .catch(error => {
        console.error('Error fetching folder structure:', error);
        folderStructureElement.textContent = 'Unable to load folder structure. Please try again later.';
      });
  }

  fetchFolderStructure();
});
