import * as params from '@params';

// No cookies, persistent identifiers, query strings, or email in analytics.
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
