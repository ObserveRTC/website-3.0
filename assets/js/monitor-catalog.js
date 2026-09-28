const catalog = document.querySelector('[data-monitor-catalog]');
if (catalog) {
  const search = catalog.querySelector('#monitor-search');
  const select = catalog.querySelector('#monitor-type');
  const monitors = [...catalog.querySelectorAll('[data-monitor]')];
  function filter() {
    const query = search.value.trim().toLowerCase();
    let visibleMembers = 0;
    let visibleMonitors = 0;
    for (const monitor of monitors) {
      const selected = !select.value || select.value === monitor.dataset.monitor;
      const nameMatches = monitor.dataset.monitor.toLowerCase().includes(query);
      let count = 0;
      for (const row of monitor.querySelectorAll('[data-field]')) {
        const matches = selected && (!query || nameMatches || row.textContent.toLowerCase().includes(query));
        row.hidden = !matches;
        if (matches) count++;
      }
      monitor.hidden = count === 0;
      if (count) visibleMonitors++;
      visibleMembers += count;
      monitor.querySelector('.field-count').textContent = `${count} member${count === 1 ? '' : 's'}`;
      if (query || select.value) monitor.open = count > 0;
      else monitor.open = false;
    }
    catalog.querySelector('.catalog-count').textContent = `${visibleMembers} member${visibleMembers === 1 ? '' : 's'} across ${visibleMonitors} monitor${visibleMonitors === 1 ? '' : 's'}`;
    catalog.querySelector('.catalog-empty').hidden = visibleMembers > 0;
  }
  search.addEventListener('input', filter);
  select.addEventListener('change', filter);
  filter();
}
