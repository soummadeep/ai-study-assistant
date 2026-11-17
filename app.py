import os
from flask import Flask

# MUST be at the top level (not indented inside any function or if-block)
app = Flask(__name__)

# --- Keep all your existing @app.route(...) and helper functions here ---


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)