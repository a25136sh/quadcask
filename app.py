import webview
from a2wsgi import ASGIMiddleware

from main import app as server

if __name__ == "__main__":
    webview.create_window(
        "Quadcask",
        ASGIMiddleware(server),
        width=1440,
        height=800
    )
    webview.start(debug=False)
