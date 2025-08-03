import webview
from a2wsgi import ASGIMiddleware

from main import app as server

if __name__ == "__main__":
    webview.create_window("Quadcask", ASGIMiddleware(server))
    webview.start(debug=False)
