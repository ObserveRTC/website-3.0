(() => {
  'use strict';

  const storedTheme = () => {
    try { return localStorage.getItem('theme'); } catch { return null; }
  };
  const preferredTheme = () => {
    const saved = storedTheme();
    return saved === 'light' || saved === 'dark' ? saved : 'light';
  };
  const setTheme = (theme) => {
    document.documentElement.setAttribute('data-bs-theme', theme);
    const button = document.getElementById('buttonColorMode');
    if (button) button.setAttribute('aria-label', `Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`);
  };

  setTheme(preferredTheme());
  window.addEventListener('DOMContentLoaded', () => {
    setTheme(preferredTheme());
    document.getElementById('buttonColorMode')?.addEventListener('click', () => {
      const theme = document.documentElement.getAttribute('data-bs-theme') === 'dark' ? 'light' : 'dark';
      try { localStorage.setItem('theme', theme); } catch { /* Theme still works without storage. */ }
      setTheme(theme);
    });
  });
})();
