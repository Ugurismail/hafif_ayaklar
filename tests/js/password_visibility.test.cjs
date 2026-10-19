const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const { test } = require('node:test');
const script = fs.readFileSync(path.join(__dirname, '../../static/js/password_visibility.js'), 'utf8');

function setup(count = 3) {
    const windows = {};
    const nodes = [];
    const inputs = Array.from({length: count}, (_, i) => ({
        id: 'password-' + i, type: 'password', value: 'unchanged',
        parentNode: {insertBefore() {}},
        form: {addEventListener(type, handler) { this[type] = handler; }},
    }));
    vm.runInNewContext(script, {
        document: {
            querySelectorAll() { return inputs; },
            createElement(tag) {
                const node = {tag, attributes: {}, children: [], events: {},
                    appendChild(child) { this.children.push(child); },
                    setAttribute(name, value) { this.attributes[name] = value; },
                    addEventListener(name, handler) { this.events[name] = handler; },
                };
                nodes.push(node);
                return node;
            },
        },
        window: {addEventListener(name, handler) { (windows[name] ||= []).push(handler); }},
    });
    return {inputs, buttons: nodes.filter(n => n.tag === 'button'), windows};
}

test('each password toggles independently without changing its value or submitting', () => {
    const {inputs, buttons} = setup();
    buttons.forEach((button, i) => {
        assert.equal(button.type, 'button');
        assert.equal(button.attributes['aria-controls'], inputs[i].id);
        assert.equal(button.attributes['aria-pressed'], 'false');
    });
    buttons[1].events.click();
    assert.deepEqual(inputs.map(i => i.type), ['password', 'text', 'password']);
    assert.equal(buttons[1].attributes['aria-pressed'], 'true');
    assert.equal(buttons[1].title, 'Şifreyi gizle');
    assert.equal(buttons[1].children[0].className, 'bi bi-eye-slash');
    buttons[1].events.click();
    assert.equal(inputs[1].type, 'password');
    assert.equal(buttons[1].title, 'Şifreyi göster');
    assert.ok(inputs.every(i => i.value === 'unchanged'));
});

test('submit and browser history events hide revealed passwords', () => {
    const {inputs, buttons, windows} = setup();
    buttons[0].events.click();
    inputs[0].form.submit();
    assert.equal(inputs[0].type, 'password');
    for (const event of ['pagehide', 'pageshow']) {
        buttons.forEach(b => b.events.click());
        windows[event].forEach(handler => handler());
        assert.ok(inputs.every(i => i.type === 'password'));
        assert.ok(buttons.every(b => b.attributes['aria-pressed'] === 'false'));
    }
});

test('no password fields is a no-op', () => assert.equal(setup(0).buttons.length, 0));
