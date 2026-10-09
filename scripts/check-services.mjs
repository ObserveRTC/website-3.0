import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';

const code = fs.readFileSync('assets/js/site-services.js', 'utf8').replace("import * as params from '@params';", '');
function fixture({ params = {}, privacy = {}, ok = true, networkError = false, analyticsError = false, synchronousAnalyticsError = false, timeoutError = false } = {}) {
  const calls = [];
  const button = { disabled: false, textContent: 'Subscribe →' };
  const status = { textContent: '' };
  let submit;
  let expire;
  const form = {
    dataset: {}, elements: { email: { value: ' reader@example.com ' } },
    reportValidity: () => true,
    querySelector: selector => selector.includes('button') ? button : status,
    reset: () => { form.elements.email.value = ''; },
    addEventListener: (_, handler) => { submit = handler; },
  };
  vm.runInNewContext(code, {
    params: { env: 'production', analyticsendpoint: 'https://ingest.observertc.org/analytics', subscribeendpoint: 'https://ingest.observertc.org/subscribe', ...params },
    navigator: privacy, window: { location: { pathname: '/docs/', search: '?secret=hidden' } },
    document: { querySelectorAll: () => [form] },
    fetch: (url, options) => {
      if (synchronousAnalyticsError && url.endsWith("/analytics")) throw new Error("blocked");
      calls.push({ url, ...options, body: JSON.parse(options.body) });
      if (timeoutError && url.endsWith('/subscribe')) {
        return new Promise((_, reject) => options.signal.addEventListener('abort', () => reject(new Error('timeout'))));
      }
      if (networkError || (analyticsError && url.endsWith('/analytics'))) return Promise.reject(new Error('offline'));
      return Promise.resolve({ ok });
    },
    Date, AbortController,
    setTimeout: (callback, duration) => {
      if (!timeoutError) return setTimeout(callback, duration);
      assert.equal(duration, 15000);
      expire = callback;
      return 1;
    },
    clearTimeout: timer => { if (!timeoutError) clearTimeout(timer); },
  });
  return { calls, form, button, status, expire: () => expire(), submit: () => submit({ preventDefault() {} }) };
}
const success = fixture();
assert.equal(success.calls[0].url, 'https://ingest.observertc.org/analytics');
assert.equal(success.calls[0].credentials, 'omit');
assert.equal(success.calls[0].keepalive, true);
assert.equal(success.calls[0].referrerPolicy, 'no-referrer');
assert.equal(success.calls[0].headers['Content-Type'], 'application/json');
assert.equal(success.calls[0].body.event, 'page_view');
assert.equal(success.calls[0].body.path, '/docs/');
assert.deepEqual(Object.keys(success.calls[0].body).sort(), ['event', 'path', 'timestamp', 'version']);
await success.submit();
assert.equal(success.calls[1].url, 'https://ingest.observertc.org/subscribe');
assert.deepEqual(Object.keys(success.calls[1].body).sort(), ['consent', 'email', 'source', 'timestamp', 'version']);
assert.equal(success.calls[1].credentials, 'omit');
assert.equal(success.calls[1].body.email, 'reader@example.com');
assert.equal(success.calls[1].body.consent, 'monthly-newsletter-v1');
assert.match(success.status.textContent, /subscribed/);
assert.equal(success.form.elements.email.value, '');
assert.equal(success.button.disabled, false);
for (const failure of [{ ok: false }, { networkError: true }]) {
  const f = fixture(failure);
  await f.submit();
  assert.match(f.status.textContent, /try again/);
  assert.equal(f.form.elements.email.value, ' reader@example.com ');
  assert.equal(f.button.disabled, false);
}
for (const options of [
  { privacy: { doNotTrack: '1' } },
  { privacy: { globalPrivacyControl: true } },
  { params: { env: 'development' } },
  { params: { analyticsendpoint: '' } },
]) assert.equal(fixture(options).calls.length, 0);
const pending = fixture();
pending.form.dataset.pending = 'true';
await pending.submit();
assert.equal(pending.calls.length, 1);
for (const options of [
  { privacy: { doNotTrack: '1' } },
  { privacy: { globalPrivacyControl: true } },
  { params: { analyticsendpoint: '' } },
  { analyticsError: true },
  { synchronousAnalyticsError: true },
]) {
  const independent = fixture(options);
  await independent.submit();
  assert.match(independent.status.textContent, /subscribed/);
  assert.equal(independent.calls.filter(call => call.url.endsWith('/subscribe')).length, 1);
}
const timed = fixture({ timeoutError: true });
const waiting = timed.submit();
await timed.submit(); // A second click during a real pending request creates no POST.
assert.equal(timed.calls.filter(call => call.url.endsWith('/subscribe')).length, 1);
timed.expire();
await waiting;
assert.match(timed.status.textContent, /try again/);
assert.equal(timed.button.disabled, false);
assert.equal(timed.form.dataset.pending, undefined);
assert.equal(timed.form.elements.email.value, ' reader@example.com ');
const config = fs.readFileSync('config/_default/params.toml', 'utf8');
assert.match(config, /analyticsEndpoint = "https:\/\/ingest\.observertc\.org\/analytics"/);
assert.match(config, /subscribeEndpoint = "https:\/\/ingest\.observertc\.org\/subscribe"/);
console.log('Service checks passed: payloads, success, failure, privacy, development, subscription independence, timeout, and duplicate submission.');
