import sys, os

ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.extend([ROOT_PATH])

from website.app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
