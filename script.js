document.addEventListener('DOMContentLoaded', () => {
  const folderStructureElement = document.getElementById('folder-structure');
  
  const EXCLUDED_FILES = [
    'README.md',
    '_config.yml',
    'index.html',
    'script.js',
    'styles.css',
    'structure.json'
  ];

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
    const fileLink = document.createElement('a');
    fileLink.textContent = name;
    fileLink.href = `https://raw.githubusercontent.com/${window.GITHUB_USERNAME}/${window.REPO_NAME}/main/${path}`;
    fileLink.target = '_blank';
    fileLink.rel = 'noopener noreferrer';
    fileElement.appendChild(fileLink);
    return fileElement;
  }

  function pathToStructure(items) {
    const root = {};
    
    items.forEach(item => {
      // Skip hidden files, excluded files, and files in hidden directories
      if (item.path.split('/').some(part => 
          part.startsWith('.') || 
          EXCLUDED_FILES.includes(part)
      )) return;
      
      const parts = item.path.split('/');
      let current = root;
      
      for (let i = 0; i < parts.length; i++) {
        const part = parts[i];
        if (i === parts.length - 1) {
          if (item.type === 'blob') {
            current[part] = null;
          }
        } else {
          current[part] = current[part] ?? {};
          current = current[part];
        }
      }
    });
    
    return root;
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

  function fetchFolderStructure(retries = 3, delay = 1000) {
    const apiUrl = `https://api.github.com/repos/${window.GITHUB_USERNAME}/${window.REPO_NAME}/git/trees/main?recursive=true`;
    
    fetch(apiUrl)
      .then(response => {
        if (!response.ok) {
          throw new Error(`Failed to fetch repository structure. Status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        const structure = pathToStructure(data.tree);
        renderFolderStructure(structure, folderStructureElement);
      })
      .catch(error => {
        console.error('Error fetching folder structure:', error);
        if (retries > 0) {
          console.log(`Retrying in ${delay}ms... (${retries} retries left)`);
          setTimeout(() => fetchFolderStructure(retries - 1, delay * 2), delay);
        } else {
          folderStructureElement.textContent = 'Unable to load folder structure. Please try again later.';
        }
      });
  }

  fetchFolderStructure();
});
