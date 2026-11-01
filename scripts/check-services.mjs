import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';

const code = fs.readFileSync('assets/js/site-services.js', 'utf8').replace("import * as params from '@params';", '');
function fixture({ params = {}, privacy = {}, code: response = 202, networkError = false, analyticsError = false, synchronousAnalyticsError = false, timeoutError = false, storage = new Map(), storageBlocked = false } = {}) {
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
    params: { analyticscontextenabled: true, env: 'production', analyticsendpoint: 'https://ingest.observertc.org/analytics', subscribeendpoint: 'https://ingest.observertc.org/subscribe', ...params },
    navigator: { userAgent: 'Mozilla/5.0 Firefox/143.0', language: 'en-US', ...privacy }, window: { crypto: { randomUUID: () => '12345678-1234-4123-8123-123456789abc' }, localStorage: { getItem: key => { if (storageBlocked) throw Error('blocked'); return storage.get(key); }, setItem: (key, value) => { if (storageBlocked) throw Error('blocked'); storage.set(key, value); } }, location: { pathname: '/docs/', search: '?secret=hidden' } },
    document: { querySelectorAll: () => [form] },
    fetch: (url, options) => {
      if (synchronousAnalyticsError && url.endsWith("/analytics")) throw new Error("blocked");
      calls.push({ url, ...options, body: JSON.parse(options.body) });
      if (timeoutError && url.endsWith('/subscribe')) {
        return new Promise((_, reject) => options.signal.addEventListener('abort', () => reject(new Error('timeout'))));
      }
      if (networkError || (analyticsError && url.endsWith('/analytics'))) return Promise.reject(new Error('offline'));
      return Promise.resolve({ status: response, ok: response >= 200 && response < 300 });
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
assert.equal(success.calls[0].body.version, 2);
assert.equal(success.calls[0].body.event, 'page_view');
assert.equal(success.calls[0].body.path, '/docs/');
assert.deepEqual(Object.keys(success.calls[0].body).sort(), ['browser', 'browserMajorVersion', 'deviceType', 'event', 'language', 'path', 'timestamp', 'version', 'visitorId']);
await success.submit();
assert.equal(success.calls[1].url, 'https://ingest.observertc.org/subscribe');
assert.deepEqual(Object.keys(success.calls[1].body).sort(), ['consent', 'email', 'source', 'timestamp', 'version']);
assert.equal(success.calls[1].credentials, 'omit');
assert.equal(success.calls[1].body.version, 2);
assert.equal(success.calls[1].body.source, 'website');
assert.equal(success.calls[1].body.email, 'reader@example.com');
assert.equal(success.calls[1].body.consent, 'monthly-newsletter-v1');
assert.equal(success.status.textContent, 'Check your inbox to confirm your subscription. The link expires in 72 hours.');
assert.equal(success.form.elements.email.value, '');
assert.equal(success.button.disabled, false);
for (const code of [200, 202, 204]) {
  const accepted = fixture({ code });
  await accepted.submit();
  assert.equal(accepted.status.textContent, 'Check your inbox to confirm your subscription. The link expires in 72 hours.');
  assert.doesNotMatch(accepted.status.textContent, /already|subscribed/i);
  assert.equal(accepted.form.elements.email.value, '');
  assert.equal(accepted.button.disabled, false);
  assert.equal(accepted.form.dataset.pending, undefined);
}
const limited = fixture({ code: 429 });
await limited.submit();
assert.equal(limited.status.textContent, 'Too many attempts. Please wait a minute and try again.');
assert.equal(limited.form.elements.email.value, ' reader@example.com ');
assert.equal(limited.button.disabled, false);
assert.equal(limited.button.textContent, 'Subscribe →');
assert.equal(limited.form.dataset.pending, undefined);
for (const failure of [{ code: 400 }, { code: 500 }, { networkError: true }]) {
  const f = fixture(failure);
  await f.submit();
  assert.equal(f.status.textContent, 'We couldn’t save your subscription. Please try again.');
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
  assert.equal(independent.status.textContent, 'Check your inbox to confirm your subscription. The link expires in 72 hours.');
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
console.log('Service checks passed: payloads, double opt-in 200/202/204, rate limiting, failure, privacy, development, subscription independence, timeout, and duplicate submission.');

const visitorStorage = new Map();
const firstVisit = fixture({ storage: visitorStorage });
const repeatVisit = fixture({ storage: visitorStorage });
assert.equal(firstVisit.calls[0].body.visitorId, repeatVisit.calls[0].body.visitorId);
assert.equal(firstVisit.calls[0].body.browser, 'Firefox');
assert.equal(firstVisit.calls[0].body.browserMajorVersion, 143);
assert.equal(firstVisit.calls[0].body.language, 'en');
assert.equal(fixture({ storageBlocked: true }).calls[0].body.visitorId, undefined);
const privateStorage = new Map();
fixture({ storage: privateStorage, privacy: { doNotTrack: '1' } });
fixture({ storage: privateStorage, privacy: { globalPrivacyControl: true } });
assert.equal(privateStorage.size, 0);
console.log('Visitor context checks passed: reuse, coarse context, blocked storage, no identifiers under DNT/GPC.');

const contextDisabled = fixture({ params: { analyticscontextenabled: false } });
assert.deepEqual(Object.keys(contextDisabled.calls[0].body).sort(), ['event', 'path', 'timestamp', 'version']);
const contextDisabledStorage = new Map();
fixture({ params: { analyticscontextenabled: false }, storage: contextDisabledStorage });
assert.equal(contextDisabledStorage.size, 0);
assert.equal(contextDisabled.calls[0].body.version, 2);
assert.match(config, /analyticsContextEnabled = true/);
for (const ua of ['Firefox/9999.0', 'Firefox/10000.0']) {
  const result = fixture({ privacy: { userAgent: ua } }).calls[0].body;
  assert.equal(result.browserMajorVersion, ua.includes('10000') ? undefined : 9999);
}
assert.ok(Buffer.byteLength(JSON.stringify(success.calls[0].body)) < 4096);
assert.ok(Buffer.byteLength(JSON.stringify(success.calls[1].body)) < 4096);
