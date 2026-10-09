// Match attribute values directly: tab names can contain spaces or punctuation.
const tabs = [...document.querySelectorAll('[data-toggle-tab]')];
const panes = [...document.querySelectorAll('[data-pane]')];
const readPreference = () => {
  try { return window.localStorage.getItem('configLangPref'); } catch { return null; }
};
function selectTabs(key) {
  const selectedTabs = tabs.filter(tab => tab.getAttribute('data-toggle-tab') === key);
  if (!selectedTabs.length) return; // Keep defaults when a saved tab isn't on this page.
  const selectedPanes = panes.filter(pane => pane.getAttribute('data-pane') === key);
  const groups = new Set(selectedTabs.map(tab => tab.closest('[role="tablist"]') || tab.parentElement));
  tabs.forEach(tab => {
    if (!groups.has(tab.closest('[role="tablist"]') || tab.parentElement)) return;
    const selected = selectedTabs.includes(tab);
    tab.classList.toggle('active', selected);
    tab.setAttribute('aria-selected', String(selected));
    const pane = panes.find(item => item.id === tab.getAttribute('aria-controls'));
    if (pane) {
      pane.classList.toggle('active', selected);
      pane.classList.toggle('show', selected);
    }
  });
  selectedPanes.forEach(pane => pane.classList.add('show', 'active'));
}
tabs.forEach(tab => tab.addEventListener('click', event => {
  event.preventDefault();
  const key = tab.getAttribute('data-toggle-tab');
  try { window.localStorage.setItem('configLangPref', key); } catch { /* Optional preference. */ }
  selectTabs(key);
}));
selectTabs(readPreference());
