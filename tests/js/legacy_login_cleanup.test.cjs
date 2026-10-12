const assert = require('node:assert/strict');
const { readFileSync } = require('node:fs');
const { resolve } = require('node:path');
const { test } = require('node:test');
const vm = require('node:vm');

const template = readFileSync(resolve(__dirname, '../../core/templates/core/_legacy_login_cleanup.html'), 'utf8');
const source = template.slice(template.indexOf('<script>') + 8, template.indexOf('</script>'));

test('removes only legacy credentials without reading or sending them', () => {
  const values = new Map([['savedPassword', 'synthetic-secret'], ['savedUsername', 'synthetic-user'], ['draft', 'keep'], ['theme', 'keep']]);
  const calls = [];
  const storage = {
    removeItem(key) { calls.push(key); values.delete(key); },
    getItem() { throw new Error('must not read credentials'); },
    setItem() { throw new Error('must not persist credentials'); },
    clear() { throw new Error('must preserve unrelated storage'); },
  };
  vm.runInNewContext(source, { window: { localStorage: storage } });
  assert.deepEqual(calls, ['savedPassword', 'savedUsername']);
  assert.deepEqual([...values], [['draft', 'keep'], ['theme', 'keep']]);
});

test('disabled storage does not break the page', () => {
  const window = Object.defineProperty({}, 'localStorage', { get() { throw new Error('storage disabled'); } });
  assert.doesNotThrow(() => vm.runInNewContext(source, { window }));
});

test('cleanup is safe on repeated visits', () => {
  const values = new Map();
  const context = { window: { localStorage: { removeItem(key) { values.delete(key); } } } };
  vm.runInNewContext(source, context);
  vm.runInNewContext(source, context);
  assert.equal(values.size, 0);
});
