const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const source = fs.readFileSync(path.join(__dirname, '../../static/js/entry_reference.js'), 'utf8');

function setup(writeText) {
  let listener;
  const messages = [];
  vm.runInNewContext(source, {
    document: { addEventListener: (_event, callback) => { listener = callback; } },
    navigator: { clipboard: { writeText } },
    showToast: (...args) => messages.push(args),
  });
  const button = { dataset: { copyEntryReference: '#123' }, disabled: false };
  const event = { target: { closest: () => button }, preventDefault() {} };
  return { listener, messages, button, event };
}

test('copies the entry reference and confirms only after clipboard success', async () => {
  const values = [];
  const state = setup(async value => values.push(value));
  await state.listener(state.event);
  assert.deepEqual(values, ['#123']);
  assert.equal(state.messages[0][1], 'success');
  assert.equal(state.button.disabled, false);
});

test('clipboard failure is reported, and the control can be retried', async () => {
  const state = setup(async () => { throw new Error('Denied'); });
  await state.listener(state.event);
  assert.equal(state.messages[0][1], 'error');
  assert.match(state.messages[0][0], /#123/);
  assert.equal(state.button.disabled, false);
});

test('ignores malformed references and unrelated clicks', async () => {
  const state = setup(async () => { throw new Error('must not run'); });
  state.button.dataset.copyEntryReference = '<img onerror=x>';
  await state.listener(state.event);
  state.event.target.closest = () => null;
  await state.listener(state.event);
  assert.equal(state.messages.length, 0);
});

test('does not start duplicate clipboard requests while pending', async () => {
  let finish;
  let calls = 0;
  const state = setup(() => { calls += 1; return new Promise(resolve => { finish = resolve; }); });
  const pending = state.listener(state.event);
  await state.listener(state.event);
  assert.equal(calls, 1);
  finish();
  await pending;
  assert.equal(state.button.disabled, false);
});
