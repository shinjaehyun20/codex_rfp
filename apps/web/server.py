from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HOST = "0.0.0.0"
PORT = 3000
WEB_ROOT = Path(__file__).parent


def run() -> None:
    handler = lambda *args, **kwargs: SimpleHTTPRequestHandler(*args, directory=str(WEB_ROOT), **kwargs)
    server = ThreadingHTTPServer((HOST, PORT), handler)
    print(f"Web scaffold serving at http://localhost:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    run()
