import * as params from '@params';

// Coarse browser context and a random, origin-local visitor ID; no fingerprint.
function analyticsContext() {
  const ua = navigator.userAgent || '';
  const match = [/\b(Edg)\/(\d+)/, /\b(Firefox)\/(\d+)/, /\b(Chrome)\/(\d+)/, /\b(Version)\/(\d+)/]
    .map(pattern => ua.match(pattern)).find(Boolean);
  const names = { Edg: 'Edge', Firefox: 'Firefox', Chrome: 'Chrome', Version: 'Safari' };
  const context = {
    browser: match ? names[match[1]] : 'Other',
    deviceType: /iPad|Tablet|Android(?!.*Mobile)/i.test(ua) ? 'tablet' : /Mobile|iPhone|Android/i.test(ua) ? 'mobile' : 'desktop',
  };
  if (match) context.browserMajorVersion = Number(match[2]);
  const language = (navigator.language || '').split('-')[0].toLowerCase();
  if (/^[a-z]{2,3}$/.test(language)) context.language = language;
  try {
    const key = 'observertc-analytics-visitor';
    let id = window.localStorage.getItem(key);
    if (!/^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(id || '')) {
      id = window.crypto.randomUUID();
      window.localStorage.setItem(key, id);
    }
    context.visitorId = id;
  } catch { /* Without storage, retain anonymous page views. */ }
  return context;
}
if (params.analyticsendpoint &&
    (params.env === 'production' || params.analyticsindevelopment) &&
    navigator.doNotTrack !== '1' && !navigator.globalPrivacyControl) {
  try {
    fetch(params.analyticsendpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'omit',
      referrerPolicy: 'no-referrer',
      keepalive: true,
      body: JSON.stringify({
        version: 1,
        event: 'page_view',
        ...analyticsContext(),
        path: window.location.pathname,
        timestamp: new Date().toISOString(),
      }),
    }).catch(() => {}); // Analytics failure must never affect reading the site.
  } catch {
    // A synchronous analytics error must not prevent subscription setup.
  }
}

document.querySelectorAll('[data-subscribe-form]').forEach((form) => {
  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    if (!form.reportValidity() || form.dataset.pending) return;
    const email = form.elements.email.value.trim();
    const button = form.querySelector('button[type="submit"]');
    const status = form.querySelector('[data-subscribe-status]');
    form.dataset.pending = 'true';
    button.disabled = true;
    button.textContent = 'Subscribing…';
    status.textContent = '';
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 15000);
    try {
      const response = await fetch(params.subscribeendpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'omit',
        referrerPolicy: 'no-referrer',
        signal: controller.signal,
        body: JSON.stringify({
          version: 1, email, source: 'website',
          consent: 'monthly-newsletter-v1',
          timestamp: new Date().toISOString(),
        }),
      });
      if (!response.ok) throw new Error('Subscription rejected');
      status.textContent = 'You’re subscribed. Thank you!';
      form.reset();
    } catch {
      status.textContent = 'We couldn’t save your subscription. Please try again.';
    } finally {
      clearTimeout(timeout);
      delete form.dataset.pending;
      button.disabled = false;
      button.textContent = 'Subscribe →';
    }
  });
});
