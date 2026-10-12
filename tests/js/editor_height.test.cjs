const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const { test } = require('node:test');

for (const template of ['edit_answer.html', 'single_answer.html']) {
    const html = fs.readFileSync(path.join(__dirname, '../../core/templates/core', template), 'utf8');
    // Execute the actual template initializer, not a copy of its behavior.
    const initializer = html.match(/document\.addEventListener\("DOMContentLoaded", function\(\) \{\s*document\.querySelectorAll\([^]*?\n\}\);/)[0];

    function editor() {
        const events = new Map();
        const textarea = {
            dataset: {}, style: {}, offsetHeight: 100,
            addEventListener(type, callback, options) {
                events.set(type, { callback, options });
            },
            dispatch(type) {
                const listener = events.get(type);
                if (!listener) return;
                listener.callback.call(this);
                if (listener.options?.once) events.delete(type);
            },
        };
        vm.runInNewContext(initializer, { document: {
            addEventListener(type, callback) { callback(); },
            querySelectorAll() { return [textarea]; },
        } });
        return textarea;
    }

    test(`${template}: leaving the editor for draft/preview does not shrink it`, () => {
        const textarea = editor();
        textarea.dispatch('focus');
        assert.equal(textarea.style.height, '300px');
        textarea.dispatch('blur');
        assert.equal(textarea.style.height, '300px');
    });

    test(`${template}: refocusing preserves a manually resized editor`, () => {
        const textarea = editor();
        textarea.dispatch('focus');
        textarea.style.height = '550px';
        textarea.dispatch('blur');
        textarea.dispatch('focus');
        assert.equal(textarea.style.height, '550px');
    });

    test(`${template}: first focus cannot shrink an already enlarged editor`, () => {
        const textarea = editor();
        textarea.offsetHeight = 600;
        textarea.dispatch('focus');
        assert.equal(textarea.style.height, '600px');
    });
}
