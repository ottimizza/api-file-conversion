from app import create_app
import os

port = int(os.environ.get("PORT", 5000))

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=port, debug=True)
