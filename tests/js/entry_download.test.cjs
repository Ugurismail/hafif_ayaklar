const assert = require('node:assert/strict');
const {readFileSync} = require('node:fs');
const {join} = require('node:path');
const {test} = require('node:test');
const vm = require('node:vm');

const source = readFileSync(join(__dirname, '../../static/js/entry_download.js'), 'utf8');
function downloader(fetch) {
  const context = {window: {}, fetch};
  vm.runInNewContext(source, context);
  return context.window.requestEntryDownload;
}
function attachment(body = 'file', type = 'application/pdf', filename = 'attachment; filename="entries.pdf"') {
  return new Response(body, {headers: {'Content-Type': type, 'Content-Disposition': filename}});
}

test('all four formats return a nonempty attachment and preserve POST/CSRF/signal', async () => {
  for (const [format, type] of Object.entries({pdf: 'application/pdf', docx: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    xlsx: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', json: 'application/json'})) {
    const body = new FormData();
    body.set('csrfmiddlewaretoken', 'test-token');
    body.set('entry_ids', '2,1');
    const signal = new AbortController().signal;
    const request = downloader(async (url, options) => {
      assert.equal(url, '/download/');
      assert.equal(options.method, 'POST');
      assert.equal(options.credentials, 'same-origin');
      assert.equal(options.cache, 'no-store');
      assert.equal(options.body, body);
      assert.equal(options.signal, signal);
      return attachment('file', type, `attachment; filename="entries.${format}"`);
    });
    const result = await request({url: '/download/', format, body, signal});
    assert.equal(result.filename, `entries.${format}`);
    assert.equal(await result.blob.text(), 'file');
  }
});

test('waits for the complete response body, not only response headers', async () => {
  let release;
  const body = new Promise(resolve => { release = resolve; });
  const response = attachment();
  response.blob = () => body;
  let completed = false;
  const promise = downloader(async () => response)({format: 'pdf'}).then(result => {
    completed = true;
    return result;
  });
  await new Promise(resolve => setImmediate(resolve));
  assert.equal(completed, false);
  release(new Blob(['complete file']));
  assert.equal(await (await promise).blob.text(), 'complete file');
});

test('decodes Unicode filenames and removes path components', async () => {
  const result = await downloader(async () => attachment('file', 'application/pdf',
    "attachment; filename*=UTF-8''U%C4%9Fur%2Fentry.pdf"))({format: 'pdf'});
  assert.equal(result.filename, 'Uğur_entry.pdf');
});

test('plain-text PDF timeout stays a readable error', async () => {
  const request = downloader(async () => new Response('PDF oluşturma süresi aşıldı.',
    {status: 503, headers: {'Content-Type': 'text/plain; charset=utf-8'}}));
  await assert.rejects(request({format: 'pdf'}), /süresi aşıldı/);
});

test('HTML failures, JSON errors and missing attachment headers are not files', async () => {
  for (const response of [new Response('<html>Login</html>', {headers: {'Content-Type': 'text/html'}}),
    new Response('{"error":"denied"}', {headers: {'Content-Type': 'application/json'}}),
    new Response('error', {status: 500})]) {
    await assert.rejects(downloader(async () => response)({format: 'pdf'}));
  }
});

test('redirects and expired sessions cannot be downloaded as documents', async () => {
  const redirected = attachment();
  Object.defineProperty(redirected, 'redirected', {value: true});
  for (const response of [redirected, new Response('', {status: 401}), new Response('', {status: 403})]) {
    await assert.rejects(downloader(async () => response)({format: 'pdf'}), /Oturumunuzu/);
  }
});

test('empty attachments are rejected', async () => {
  await assert.rejects(downloader(async () => attachment(''))({format: 'pdf'}), /boş/);
});

test('abort and network errors reach the controller without automatic retries', async () => {
  for (const error of [new DOMException('Cancelled', 'AbortError'), new TypeError('Network error')]) {
    let requests = 0;
    const request = downloader(async () => { requests++; throw error; });
    await assert.rejects(request({format: 'pdf'}), actual => actual === error);
    assert.equal(requests, 1);
  }
});
