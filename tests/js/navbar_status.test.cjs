const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const source = fs.readFileSync(path.join(__dirname, '../../static/js/navbar_status.js'), 'utf8');
const flush = () => new Promise(resolve => setImmediate(resolve));

function setup(fetcher, hasBadge = true) {
    let now = 10000;
    const events = {};
    const windowEvents = {};
    const timers = [];
    const intervals = [];
    const calls = [];
    const badge = { textContent: '3', style: { display: 'inline-block' } };
    const document = { hidden: false, getElementById: id => hasBadge && id === 'notification-badge' ? badge : null,
        addEventListener: (name, cb) => { events[name] = cb; } };
    vm.runInNewContext(source, {
        document, window: { addEventListener: (name, cb) => { windowEvents[name] = cb; } },
        Date: { now: () => now }, AbortController,
        fetch: (...args) => { calls.push(args); return fetcher(...args); },
        setTimeout: (cb, ms) => { timers.push({cb, ms}); return timers.length; }, clearTimeout: () => {},
        setInterval: (cb, ms) => { intervals.push({cb, ms}); },
    });
    events.DOMContentLoaded();
    return { badge, document, events, windowEvents, intervals, timers, calls,
        advance: () => { now += 15000; } };
}
const payload = count => ({ ok: true, headers: { get: () => 'application/json' },
    json: async () => ({ notification_count: count, message_count: 0, online_chat_count: 0 }) });

test('initial refresh works without a search form and polls every 15 seconds', async () => {
    let count = 4;
    const state = setup(async () => payload(count));
    await flush();
    assert.equal(state.badge.textContent, '4');
    assert.equal(state.calls[0][1].cache, 'no-store');
    assert.equal(state.intervals[0].ms, 15000);
    count = 0;
    state.advance();
    await state.intervals[0].cb();
    assert.equal(state.badge.style.display, 'none');
});

test('hidden tabs do not poll; returning to a tab immediately refreshes', async () => {
    const state = setup(async () => payload(1));
    await flush();
    state.advance();
    state.document.hidden = true;
    await state.intervals[0].cb();
    assert.equal(state.calls.length, 1);
    state.document.hidden = false;
    await state.events.visibilitychange();
    assert.equal(state.calls.length, 2);
    await state.windowEvents.focus();
    assert.equal(state.calls.length, 2);
});

test('network failure keeps server count and allows the next retry', async () => {
    let fail = true;
    const state = setup(async () => { if (fail) throw Error('offline'); return payload(105); });
    await flush();
    assert.equal(state.badge.textContent, '3');
    fail = false;
    state.advance();
    await state.intervals[0].cb();
    assert.equal(state.badge.textContent, '99+');
});

test('an expired session HTML response does not wipe the existing count', async () => {
    const state = setup(async () => ({ ok: true, headers: { get: () => 'text/html' } }));
    await flush();
    assert.equal(state.badge.textContent, '3');
});

test('a pending request is not duplicated and timed out requests can retry', async () => {
    const state = setup((_url, options) => new Promise((_resolve, reject) => {
        options.signal.addEventListener('abort', () => reject(Error('timeout')));
    }));
    state.advance();
    await state.intervals[0].cb();
    assert.equal(state.calls.length, 1);
    state.timers[0].cb();
    await flush();
    state.advance();
    state.intervals[0].cb();
    assert.equal(state.calls.length, 2);
    state.timers[1].cb();
    await flush();
});

test('guests start no requests or timers', async () => {
    const state = setup(async () => payload(4), false);
    await flush();
    assert.equal(state.calls.length, 0);
    assert.equal(state.intervals.length, 0);
});
