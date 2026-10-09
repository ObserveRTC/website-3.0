// Keep documentation navigation stable across full-page article loads.
(() => {
  const menus = document.querySelectorAll('.section-nav.docs-links');
  const sidebar = document.querySelector('.docs-layout .docs-sidebar');
  const read = key => {
    try { return JSON.parse(sessionStorage.getItem(key)); } catch { return null; }
  };
  const write = (key, value) => {
    try { sessionStorage.setItem(key, JSON.stringify(value)); } catch { /* Optional UI state. */ }
  };
  const sections = read('docs-navigation-sections') ?? {};
  menus.forEach(menu => {
    menu.querySelectorAll('details').forEach(details => {
      const name = details.querySelector('summary')?.textContent.trim();
      if (!name) return;
      if (typeof sections[name] === 'boolean') details.open = sections[name];
      // Always expose the article that is currently being read.
      if (details.querySelector('[aria-current="page"]')) details.open = true;
      details.addEventListener('toggle', () => {
        sections[name] = details.open;
        write('docs-navigation-sections', sections);
      });
    });
  });
  const containers = [
    [sidebar, 'docs-navigation-scroll'],
    [document.querySelector('#offcanvasNavSection .offcanvas-body'), 'docs-navigation-mobile-scroll'],
  ];
  containers.forEach(([container, key]) => {
    if (!container) return;
    const saved = read(key);
    let restoring = true;
    let interacted = false;
    const saveScroll = () => {
      // A hidden desktop sidebar has scrollTop 0; never let it overwrite
      // the desktop position when navigating from the mobile menu.
      if (!restoring && container.clientHeight > 0) write(key, container.scrollTop);
    };
    const restore = () => {
      if (interacted || container.clientHeight === 0) return;
      restoring = true;
      if (typeof saved === 'number') container.scrollTop = saved;
      const active = container.querySelector('[aria-current="page"]');
      if (active) {
        const item = active.getBoundingClientRect();
        const bounds = container.getBoundingClientRect();
        if (item.top < bounds.top || item.bottom > bounds.bottom) {
          // Reveal only as much as needed; don't move the menu to its top.
          container.scrollTop += item.top < bounds.top
            ? item.top - bounds.top
            : item.bottom - bounds.bottom;
        }
      }
      requestAnimationFrame(() => { restoring = false; });
    };
    container.addEventListener('scroll', saveScroll, { passive: true });
    container.addEventListener('pointerdown', () => { interacted = true; restoring = false; }, { passive: true });
    container.addEventListener('wheel', () => { interacted = true; restoring = false; }, { passive: true });
    container.addEventListener('click', saveScroll, true);
    window.addEventListener('pagehide', saveScroll);
    // Layout and font loading can clamp an early scrollTop assignment to 0.
    requestAnimationFrame(restore);
    window.addEventListener('load', restore, { once: true });
    document.fonts?.ready.then(restore);
    const drawer = container.closest('.offcanvas');
    drawer?.addEventListener('shown.bs.offcanvas', restore);
  });
})();
