const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const {test} = require('node:test');
const script = fs.readFileSync(path.join(__dirname, '../../static/js/reference_history.js'), 'utf8');

function setup(fetcher) {
    let counter = 0, field;
    const requests = [], listeners = {};
    const buttons = [{disabled: false}, {disabled: true}];
    const form = {
        querySelector(selector) { return selector.includes('reference_context') ? field : {value: 'Test title'}; },
        querySelectorAll() { return buttons; },
        appendChild(node) { field = node; },
        addEventListener(name, handler) { listeners[name] = handler; },
        removeEventListener(name) { delete listeners[name]; },
    };
    const textarea = {form, readOnly: false};
    const window = {};
    vm.runInNewContext(script, {
        window, crypto: {randomUUID: () => 'uuid-' + (++counter)},
        location: {href: 'https://example.test/write/?draft_id=12'},
        URL, AbortController, setTimeout, clearTimeout,
        document: {
            createElement: () => ({}), addEventListener() {},
            querySelector: () => ({content: 'csrf-token'}),
            getElementById: () => ({dataset: {historyUrl: '/kaynak-gecmisim/ekle/'}}),
        },
        fetch: async (url, options) => {
            requests.push({url, options, payload: JSON.parse(options.body)});
            return fetcher(requests.length);
        },
    });
    return {api: window.ReferenceHistory, textarea, buttons, requests, listeners};
}
const success = () => ({ok: true, headers: {get: () => 'application/json'}, json: async () => ({id: 1})});

test('retry keeps event ID, a new insertion gets a new ID, context stays stable', async () => {
    const state = setup(n => n === 1 ? {ok: false, headers: {get: () => 'text/html'}} : success());
    await assert.rejects(state.api.record(state.textarea, '4', '10'));
    await state.api.record(state.textarea, '4', '10');
    await state.api.record(state.textarea, '4', '10');
    const payloads = state.requests.map(r => r.payload);
    assert.equal(payloads[0].event_id, payloads[1].event_id);
    assert.notEqual(payloads[1].event_id, payloads[2].event_id);
    assert.equal(new Set(payloads.map(p => p.context_id)).size, 1);
    assert.equal(payloads[0].draft_id, '12');
    assert.equal(payloads[0].reference_id, 4);
    assert.equal(state.requests[0].options.headers['X-CSRFToken'], 'csrf-token');
});

test('pending request blocks submit and restores exact controls on success', async () => {
    let resolve;
    const state = setup(() => new Promise(done => { resolve = done; }));
    const pending = state.api.record(state.textarea, 4, '');
    assert.ok(state.textarea.readOnly);
    assert.ok(state.buttons.every(b => b.disabled));
    let prevented = false, stopped = false;
    state.listeners.submit({preventDefault() { prevented = true; }, stopImmediatePropagation() { stopped = true; }});
    assert.ok(prevented && stopped);
    resolve(success()); await pending;
    assert.equal(state.textarea.readOnly, false);
    assert.deepEqual(state.buttons.map(b => b.disabled), [false, true]);
    assert.equal(state.listeners.submit, undefined);
});

test('failed requests restore controls and propagate server error', async () => {
    const state = setup(() => ({ok: false, headers: {get: () => 'application/json'}, json: async () => ({error: 'Limit reached'})}));
    await assert.rejects(state.api.record(state.textarea, 4, ''), /Limit reached/);
    assert.equal(state.textarea.readOnly, false);
    assert.deepEqual(state.buttons.map(b => b.disabled), [false, true]);
    assert.equal(state.listeners.submit, undefined);
});
