/* AlgoQuest - Adventure Page JavaScript */

document.addEventListener('DOMContentLoaded', () => {
  const questNodes = document.querySelectorAll('.quest-node');
  const panelPathName = document.getElementById('panel-path-name');
  const panelXp = document.getElementById('panel-xp');
  const panelTitle = document.getElementById('panel-title');
  const panelDesc = document.getElementById('panel-desc');
  const panelBoostStat = document.getElementById('panel-boost-stat');
  const panelBoostVal = document.getElementById('panel-boost-val');
  const statusSelectedNode = document.getElementById('status-selected-node');

  // Node details mapping
  const questData = {
    '1': {
      path: 'TRAVERSAL TRAIL',
      xp: '+85 XP',
      title: 'The Lost Maximum',
      desc: 'Traverse an un-ordered array to discover the single largest integer value while updating memory pointers on each step.',
      boostStat: 'traversal bounds',
      boostVal: '+5% Mastery'
    },
    '2': {
      path: 'SEARCH PATH',
      xp: '+75 XP',
      title: 'Search in the Mist',
      desc: 'Thick fog obscures the trail. You are searching for an exact runic key (target value) in an unsorted array of path stones. Locate its index or report -1 if unreachable.',
      boostStat: 'decomposition',
      boostVal: '+8% Mastery'
    },
    '3': {
      path: 'RUNIC GROVE',
      xp: '+90 XP',
      title: 'The Frequency Village',
      desc: 'Count unique frequencies of runic symbols across array elements using hash map memory tables.',
      boostStat: 'frequency mapping',
      boostVal: '+10% Mastery'
    },
    '4': {
      path: 'TWIN MONOLITHS',
      xp: '+110 XP',
      title: 'Two-Pointer Monoliths',
      desc: 'Manipulate left and right boundary pointers towards the center to identify target sum pairs in sorted arrays.',
      boostStat: 'two-pointer logic',
      boostVal: '+12% Mastery'
    },
    '5': {
      path: 'KADANE\'S CITADEL',
      xp: '+150 XP',
      title: 'Trial of the Array Guardian',
      desc: 'Face the ultimate guardian in a high-stakes duel! Solve maximum subarray contiguous sums using dynamic state tracking.',
      boostStat: 'kadane algorithm',
      boostVal: '+20% Mastery'
    }
  };

  questNodes.forEach(node => {
    node.addEventListener('click', () => {
      // Remove active-quest visual from others
      questNodes.forEach(n => n.classList.remove('active-quest'));
      node.classList.add('active-quest');

      const nodeId = node.getAttribute('data-node-id');
      const data = questData[nodeId];
      if (data) {
        if (panelPathName) panelPathName.textContent = data.path;
        if (panelXp) panelXp.textContent = data.xp;
        if (panelTitle) panelTitle.textContent = data.title;
        if (panelDesc) panelDesc.textContent = data.desc;
        if (panelBoostStat) panelBoostStat.textContent = data.boostStat;
        if (panelBoostVal) panelBoostVal.textContent = data.boostVal;
        if (statusSelectedNode) statusSelectedNode.textContent = `${data.title} in ${data.path}`;
      }
    });
  });

  // Map vs List Toggle Switch
  const mapToggleBtn = document.getElementById('toggle-map');
  const listToggleBtn = document.getElementById('toggle-list');
  const mapViewport = document.getElementById('map-viewport');

  if (mapToggleBtn && listToggleBtn && mapViewport) {
    mapToggleBtn.addEventListener('click', () => {
      mapToggleBtn.classList.add('active');
      listToggleBtn.classList.remove('active');
      mapViewport.style.flexDirection = 'column';
      mapViewport.style.justifyContent = 'space-between';
    });

    listToggleBtn.addEventListener('click', () => {
      listToggleBtn.classList.add('active');
      mapToggleBtn.classList.remove('active');
      mapViewport.style.flexDirection = 'column';
      mapViewport.style.justifyContent = 'flex-start';
      mapViewport.style.gap = '1rem';
    });
  }
});
