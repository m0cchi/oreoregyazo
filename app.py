from flask import Flask, request, abort, send_from_directory
from uuid import uuid4
from urllib.parse import urljoin
import os

app = Flask(__name__)
ENV_FORMAT = 'OREOREGYAZO_{}'
app.config['IMAGE_URL'] = os.getenv(ENV_FORMAT.format('URL'), 'http://localhost:3000/images/')
app.config['IMAGE_DIR'] = os.getenv(ENV_FORMAT.format('DIR'), './images')

@app.route('/')
def index():
    return ''

@app.route('/images/<filename>')
def image(filename):
    return send_from_directory(app.config['IMAGE_DIR'], filename)

@app.route('/upload.cgi', methods=['POST'])
def save():
    f = request.files['imagedata']
    count = 0
    while True:
        filepath = os.path.join(app.config['IMAGE_DIR'],'./{}.png'.format(uuid4()))
        filepath = os.path.abspath(filepath)
        if not os.path.exists(filepath):
            break
        count += 1
        if count > 10:
            abort(500, "can't create file")
    f.save(filepath)
    return urljoin(app.config['IMAGE_URL'], os.path.basename(filepath))

if __name__ == '__main__':
    app.debug = os.getenv(ENV_FORMAT.format('DEBUG'), 'DEBUG') == 'DEBUG'
    app.run(host=os.getenv(ENV_FORMAT.format('HOST'), '0.0.0.0'),
            port=int(os.getenv(ENV_FORMAT.format('PORT'), 3000)))
