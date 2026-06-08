from http.server import HTTPServer, BaseHTTPRequestHandler

HTML_UI = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Platomics Number Converter</title>
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    font-family: 'Segoe UI', system-ui, sans-serif;
    background: #0f0f13;
    color: #e8e8f0;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
  }

  .container { width: 100%; max-width: 520px; }

  .header { text-align: center; margin-bottom: 2.5rem; }
  .header h1 { font-size: 1.75rem; font-weight: 600; letter-spacing: -0.02em; color: #fff; }
  .header p  { font-size: 0.875rem; color: #7a7a8c; margin-top: 0.5rem; }

  .card {
    background: #1a1a24;
    border: 1px solid #2e2e3e;
    border-radius: 16px;
    padding: 2rem;
  }

  .row {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .row-top {
    display: flex;
    flex-direction: column;
    gap: 6px;
  }

  .row-bottom {
    display: grid;
    grid-template-columns: 1fr 36px 1fr;
    gap: 12px;
    align-items: end;
  }

  .field { display: flex; flex-direction: column; gap: 6px; }
  .field label { font-size: 0.7rem; letter-spacing: 0.08em; text-transform: uppercase; color: #5a5a72; }

  input, select {
    background: #0f0f13;
    border: 1px solid #2e2e3e;
    border-radius: 10px;
    color: #e8e8f0;
    font-family: 'Cascadia Code', 'Fira Code', monospace;
    font-size: 0.95rem;
    padding: 11px 14px;
    outline: none;
    transition: border-color 0.15s;
    width: 100%;
  }
  input:focus, select:focus { border-color: #5b5bd6; }
  input::placeholder { color: #3a3a52; }
  select option { background: #1a1a24; }

  .arrow {
    color: #3a3a52;
    font-size: 1.1rem;
    text-align: center;
    display: flex;
    align-items: center;
    justify-content: center;
    padding-top: 22px;
  }

  .url-bar {
    margin-top: 1.25rem;
    background: #0f0f13;
    border: 1px solid #2e2e3e;
    border-radius: 10px;
    padding: 10px 14px;
    font-family: 'Cascadia Code', 'Fira Code', monospace;
    font-size: 0.75rem;
    color: #5a5a72;
    word-break: break-all;
  }
  .url-bar span { color: #5b5bd6; }

  .btn {
    margin-top: 1.25rem;
    width: 100%;
    padding: 13px;
    background: #5b5bd6;
    color: #fff;
    border: none;
    border-radius: 10px;
    font-family: inherit;
    font-size: 0.95rem;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.15s, transform 0.1s;
    letter-spacing: 0.01em;
  }
  .btn:hover  { background: #4848c2; }
  .btn:active { transform: scale(0.98); }

  .result {
    margin-top: 1.25rem;
    background: #0f0f13;
    border: 1px solid #2e2e3e;
    border-radius: 10px;
    padding: 1.25rem 1.5rem;
    display: none;
    animation: fadeIn 0.2s ease;
  }
  .result.show { display: block; }
  .result-label { font-size: 0.7rem; letter-spacing: 0.08em; text-transform: uppercase; color: #5a5a72; margin-bottom: 8px; }
  .result-value { font-family: 'Cascadia Code', 'Fira Code', monospace; font-size: 1.6rem; color: #5b5bd6; word-break: break-all; }

  .error { color: #e05c5c; font-size: 0.82rem; margin-top: 10px; min-height: 18px; }

  .chips-section { margin-top: 1.75rem; }
  .chips-label  { font-size: 0.7rem; letter-spacing: 0.08em; text-transform: uppercase; color: #3a3a52; margin-bottom: 10px; }
  .chips { display: flex; flex-wrap: wrap; gap: 8px; }
  .chip {
    font-family: 'Cascadia Code', 'Fira Code', monospace;
    font-size: 0.75rem;
    color: #5a5a72;
    background: #0f0f13;
    border: 1px solid #2e2e3e;
    border-radius: 20px;
    padding: 5px 14px;
    cursor: pointer;
    transition: border-color 0.15s, color 0.15s;
  }
  .chip:hover { border-color: #5b5bd6; color: #a0a0f0; }

  .divider { border: none; border-top: 1px solid #2e2e3e; margin: 1.75rem 0; }

  .api-section h3 { font-size: 0.8rem; color: #5a5a72; letter-spacing: 0.05em; text-transform: uppercase; margin-bottom: 10px; }
  .api-row { font-family: 'Cascadia Code', 'Fira Code', monospace; font-size: 0.78rem; color: #5a5a72; margin-bottom: 6px; }
  .api-row span { color: #5b5bd6; }
  .api-row em   { color: #a0a0a0; font-style: normal; }

  @keyframes fadeIn { from { opacity: 0; transform: translateY(4px); } to { opacity: 1; transform: none; } }
</style>
</head>
<body>
<div class="container">

  <div class="header">
    <h1>Number Converter</h1>
    <p>Convert between decimal, binary, and hexadecimal</p>
  </div>

  <div class="card">
    <div class="row">
      <div class="row-top">
        <div class="field">
          <label>Value</label>
          <input id="val" type="text" placeholder="e.g. 255" oninput="updatePreview()" onkeydown="if(event.key==='Enter') convert()"/>
        </div>
      </div>
      <div class="row-bottom">
        <div class="field">
          <label>From</label>
          <select id="from" onchange="updatePreview()">
            <option value="dec">dec</option>
            <option value="bin">bin</option>
            <option value="hex">hex</option>
          </select>
        </div>
        <div class="arrow">→</div>
        <div class="field">
          <label>To</label>
          <select id="to" onchange="updatePreview()">
            <option value="hex">hex</option>
            <option value="bin">bin</option>
            <option value="dec">dec</option>
          </select>
        </div>
      </div>
    </div>

    <div class="url-bar" id="url-bar">
      GET <span id="url-text">http://localhost:8080/convert/...</span>
    </div>

    <div class="error" id="err"></div>
    <button class="btn" onclick="convert()">Convert</button>

    <div class="result" id="result">
      <div class="result-label">Result</div>
      <div class="result-value" id="result-value">—</div>
    </div>

    <div class="chips-section">
      <div class="chips-label">Quick examples</div>
      <div class="chips">
        <span class="chip" onclick="loadExample('255','dec','hex')">255 dec → hex</span>
        <span class="chip" onclick="loadExample('ff','hex','bin')">ff hex → bin</span>
        <span class="chip" onclick="loadExample('1010','bin','dec')">1010 bin → dec</span>
        <span class="chip" onclick="loadExample('42','dec','bin')">42 dec → bin</span>
        <span class="chip" onclick="loadExample('1a3f','hex','dec')">1a3f hex → dec</span>
      </div>
    </div>

    <hr class="divider"/>

    <div class="api-section">
      <h3>API endpoint</h3>
      <div class="api-row">GET <span>/convert/&lt;value&gt;/&lt;from&gt;/&lt;to&gt;</span></div>
      <div class="api-row">GET <span>/health</span> <em>→ OK</em></div>
      <div class="api-row">GET <span>/</span> <em>→ this UI</em></div>
    </div>
  </div>

</div>
<script>
  function updatePreview() {
    const val  = document.getElementById('val').value.trim() || '...';
    const from = document.getElementById('from').value;
    const to   = document.getElementById('to').value;
    document.getElementById('url-text').textContent =
      'http://localhost:8080/convert/' + val + '/' + from + '/' + to;
    document.getElementById('err').textContent = '';
  }

  function convert() {
    const val  = document.getElementById('val').value.trim();
    const from = document.getElementById('from').value;
    const to   = document.getElementById('to').value;
    const errEl   = document.getElementById('err');
    const box     = document.getElementById('result');
    const outEl   = document.getElementById('result-value');

    errEl.textContent = '';
    if (!val) { errEl.textContent = 'Please enter a value.'; box.classList.remove('show'); return; }

    // Call the real API
    fetch('/convert/' + encodeURIComponent(val) + '/' + from + '/' + to)
      .then(r => r.text().then(t => ({ ok: r.ok, text: t })))
      .then(({ ok, text }) => {
        if (!ok) { errEl.textContent = text; box.classList.remove('show'); return; }
        outEl.textContent = text;
        box.classList.add('show');
      })
      .catch(() => { errEl.textContent = 'Could not reach the server.'; });
  }

  function loadExample(v, f, t) {
    document.getElementById('val').value = v;
    document.getElementById('from').value = f;
    document.getElementById('to').value = t;
    updatePreview();
    convert();
  }

  updatePreview();
</script>
</body>
</html>
"""


def parse_value(value, fmt):
    """Parse a string value based on its format into an integer."""
    try:
        if fmt == "dec":
            return int(value, 10)
        elif fmt == "bin":
            return int(value, 2)
        elif fmt == "hex":
            return int(value, 16)
        else:
            return None, f"Unknown format '{fmt}'. Use dec, bin, or hex."
    except ValueError:
        return None, f"Value '{value}' is not valid {fmt} format."


def convert_value(integer, fmt):
    """Convert an integer to the target format string."""
    if fmt == "dec":
        return str(integer)
    elif fmt == "bin":
        return bin(integer)[2:]   # strip '0b' prefix
    elif fmt == "hex":
        return hex(integer)[2:]   # strip '0x' prefix
    else:
        return None


class ConverterHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        # --- Health check endpoint ---
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"OK")
            return

        # --- Convert endpoint ---
        if self.path.startswith("/convert/"):
            parts = self.path.strip("/").split("/")

            if len(parts) != 4:
                self.send_response(400)
                self.send_header("Content-Type", "text/plain")
                self.end_headers()
                self.wfile.write(b"Bad request. Usage: /convert/<value>/<input-format>/<output-format>\n")
                return

            _, value, input_fmt, output_fmt = parts

            valid_formats = {"dec", "bin", "hex"}

            if input_fmt not in valid_formats:
                self.send_response(400)
                self.send_header("Content-Type", "text/plain")
                self.end_headers()
                self.wfile.write(f"Invalid input-format '{input_fmt}'. Use dec, bin, or hex.\n".encode())
                return

            if output_fmt not in valid_formats:
                self.send_response(400)
                self.send_header("Content-Type", "text/plain")
                self.end_headers()
                self.wfile.write(f"Invalid output-format '{output_fmt}'. Use dec, bin, or hex.\n".encode())
                return

            result = parse_value(value, input_fmt)
            if isinstance(result, tuple):
                self.send_response(400)
                self.send_header("Content-Type", "text/plain")
                self.end_headers()
                self.wfile.write(result[1].encode())
                return

            converted = convert_value(result, output_fmt)
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(converted.encode())
            return

        # --- Root path: serve the HTML UI ---
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(HTML_UI.encode())

    def log_message(self, format, *args):
        print(f"[REQUEST] {self.address_string()} - {format % args}")


if __name__ == "__main__":
    HOST = "0.0.0.0"
    PORT = 8080
    server = HTTPServer((HOST, PORT), ConverterHandler)
    print(f"Converter API running on http://{HOST}:{PORT}")
    print(f"  UI:      http://localhost:{PORT}/")
    print(f"  API:     http://localhost:{PORT}/convert/<value>/<from>/<to>")
    print(f"  Health:  http://localhost:{PORT}/health")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")