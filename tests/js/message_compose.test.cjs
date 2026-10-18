const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const { test } = require('node:test');

const script = fs.readFileSync(path.join(__dirname, '../../static/js/message_compose.js'), 'utf8');

function compose() {
    const keyHandlers = {};
    const formHandlers = {};
    const windowHandlers = {};
    const attributes = new Map();
    const button = { disabled: false };
    const input = {
        value: 'Hello', error: '',
        addEventListener(type, handler) { keyHandlers[type] = handler; },
        setCustomValidity(message) { this.error = message; },
        reportValidity() {},
    };
    let posts = 0;
    const form = {
        querySelector(selector) { return selector.startsWith('textarea') ? input : button; },
        addEventListener(type, handler) { formHandlers[type] = handler; },
        setAttribute(name, value) { attributes.set(name, value); },
        removeAttribute(name) { attributes.delete(name); },
        requestSubmit(submitter) {
            assert.equal(submitter, button);
            if (!input.value || input.error || input.value.length > 5000) return;
            const event = { defaultPrevented: false, preventDefault() { this.defaultPrevented = true; } };
            formHandlers.submit(event);
            if (!event.defaultPrevented) posts++;
        },
    };
    vm.runInNewContext(script, {
        document: { querySelector() { return form; } },
        window: { addEventListener(type, handler) { windowHandlers[type] = handler; } },
    });
    return {
        input, button, form, attributes,
        posts: () => posts,
        change(value) { input.value = value; keyHandlers.input(); },
        restore() { windowHandlers.pageshow(); },
        key(options = {}) {
            const event = { key: 'Enter', defaultPrevented: false, ...options,
                preventDefault() { this.defaultPrevented = true; } };
            keyHandlers.keydown(event);
            return event;
        },
    };
}

test('Enter submits once and locks the pending form', () => {
    const page = compose();
    assert.equal(page.key().defaultPrevented, true);
    page.key();
    page.form.requestSubmit(page.button);
    assert.equal(page.posts(), 1);
    assert.equal(page.button.disabled, true);
    assert.equal(page.attributes.get('aria-busy'), 'true');
});

test('Shift+Enter, modifiers and composition keep native editing', () => {
    for (const options of [{ shiftKey: true }, { ctrlKey: true }, { altKey: true },
        { metaKey: true }, { isComposing: true }, { keyCode: 229 }, { key: 'a' }]) {
        const page = compose();
        assert.equal(page.key(options).defaultPrevented, false);
        assert.equal(page.posts(), 0);
    }
});

test('key repeat and already handled Enter never submit', () => {
    const page = compose();
    page.key({ repeat: true });
    page.key({ defaultPrevented: true });
    assert.equal(page.posts(), 0);
});

test('empty, whitespace and invalid input never send; editing clears validation', () => {
    const page = compose();
    for (const value of ['', ' \n ', 'a'.repeat(5001)]) {
        page.change(value);
        page.key();
        assert.equal(page.posts(), 0);
        assert.equal(page.button.disabled, false);
    }
    page.change('First line\nSecond line');
    page.key();
    assert.equal(page.posts(), 1);
    assert.equal(page.input.value, 'First line\nSecond line');
});

test('browser history restore unlocks the compose form', () => {
    const page = compose();
    page.key();
    page.restore();
    assert.equal(page.button.disabled, false);
    assert.equal(page.attributes.has('aria-busy'), false);
    page.change('Another message');
    page.key();
    assert.equal(page.posts(), 2);
});

test('absent compose form is a no-op', () => {
    assert.doesNotThrow(() => vm.runInNewContext(script, { document: { querySelector() { return null; } } }));
});
