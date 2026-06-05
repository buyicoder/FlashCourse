"""
FlashCourse local proxy — forwards requests to Anthropic API.
Reads API key from ANTHROPIC_API_KEY env var, .env file, or Claude config.

Usage: python proxy.py
Then open app.html — no API key needed in the browser.
"""
import http.server
import json
import os
import urllib.request
import sys
from pathlib import Path

PORT = 18765
ANTHROPIC_URL = "https://api.anthropic.com/v1/messages"

def find_api_key():
    """Try to find the Anthropic API key from various sources."""
    # 1. Environment variable
    key = os.environ.get("ANTHROPIC_API_KEY")
    if key: return key

    # 2. .env file in same directory
    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            if line.startswith("ANTHROPIC_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")

    # 3. Claude Code config (Windows)
    try:
        config_path = Path.home() / ".claude" / "credentials.json"
        if config_path.exists():
            config = json.loads(config_path.read_text())
            # Try various key paths in Claude config
            for k in ["anthropicApiKey", "apiKey", "anthropic_api_key"]:
                if config.get(k):
                    return config[k]
    except Exception:
        pass

    return None

class ProxyHandler(http.server.BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, Anthropic-Version")
        self.end_headers()

    def do_POST(self):
        if self.path != "/v1/messages":
            self.send_response(404)
            self.end_headers()
            return

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        try:
            req = urllib.request.Request(ANTHROPIC_URL, data=body, method="POST")
            req.add_header("Content-Type", "application/json")
            req.add_header("x-api-key", API_KEY)
            req.add_header("anthropic-version", "2023-06-01")

            with urllib.request.urlopen(req) as resp:
                response_body = resp.read()

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(response_body)

        except urllib.error.HTTPError as e:
            self.send_response(e.code)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(e.read())

    def log_message(self, format, *args):
        # Suppress default logging
        pass

if __name__ == "__main__":
    API_KEY = find_api_key()

    if API_KEY:
        masked = API_KEY[:7] + "..." + API_KEY[-4:]
        print(f"✅ API Key found: {masked}")
    else:
        print("❌ No API key found.")
        print("   Set ANTHROPIC_API_KEY environment variable, or")
        print(f"   Create .env file next to proxy.py with: ANTHROPIC_API_KEY=sk-ant-...")
        key = input("   Or paste your API key now: ").strip()
        if key:
            API_KEY = key
            # Save to .env for next time
            env_file = Path(__file__).parent / ".env"
            env_file.write_text(f"ANTHROPIC_API_KEY={key}")
            print(f"   ✅ Saved to .env")
        else:
            print("   Exiting.")
            sys.exit(1)

    print(f"\n⚡ FlashCourse proxy starting on http://localhost:{PORT}")
    print(f"   Open app.html in your browser and start learning!\n")

    server = http.server.HTTPServer(("127.0.0.1", PORT), ProxyHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Proxy stopped.")
        server.server_close()
