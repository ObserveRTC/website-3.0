import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
const code = fs.readFileSync('assets/js/tabs.js', 'utf8');
function fixture(preference, blocked = false) {
  const group = {};
  const element = (key, id) => {
    const classes = new Set();
    return { id, classes, classList: { toggle: (name, on) => on ? classes.add(name) : classes.delete(name), add: (...names) => names.forEach(name => classes.add(name)) }, getAttribute: name => name === 'aria-controls' ? id : key, setAttribute() {}, closest: () => group, addEventListener(_, handler) { this.click = handler; } };
  };
  const tabs = [element('client only', 'client'), element('server "quoted"', 'server')];
  const panes = [element('client only', 'client'), element('server "quoted"', 'server')];
  tabs[0].classes.add('active'); panes[0].classes.add('active');
  vm.runInNewContext(code, { document: { querySelectorAll: selector => {
    assert.ok(['[data-toggle-tab]', '[data-pane]'].includes(selector));
    return selector === '[data-pane]' ? panes : tabs;
  } }, window: { localStorage: { getItem() { if (blocked) throw Error('blocked'); return preference; }, setItem() { if (blocked) throw Error('blocked'); } } } });
  return { tabs, panes };
}
let f = fixture('client only');
assert.ok(f.tabs[0].classes.has('active'));
f.tabs[1].click({ preventDefault() {} });
assert.ok(f.panes[1].classes.has('active'));
assert.ok(!f.panes[0].classes.has('active'));
f = fixture('not on this page');
assert.ok(f.tabs[0].classes.has('active'));
fixture('client only', true).tabs[1].click({ preventDefault() {} });
const policy = fs.readFileSync('netlify.toml', 'utf8').match(/connect-src ([^;]+);/)[1];
assert.equal(policy, "'self' https://ingest.observertc.org");
console.log('Tab checks passed: spaces, punctuation, absent preferences, unavailable storage; ingestion CSP allows only the intended origin.');
