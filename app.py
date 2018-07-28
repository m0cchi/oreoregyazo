from flask import Flask, request, abort, send_from_directory
from uuid import uuid4
from urllib.parse import urljoin
import os
from flask_cors import CORS
from kafka import KafkaProducer

app = Flask(__name__)
ENV_FORMAT = 'OREOREGYAZO_{}'
app.config['IMAGE_URL'] = os.getenv(ENV_FORMAT.format('URL'), 'http://localhost:3000/images/')
app.config['IMAGE_DIR'] = os.getenv(ENV_FORMAT.format('DIR'), './images')
CORS(app, resources={'/images/*': {'origins': os.getenv(ENV_FORMAT.format('ALLOW_CORS_HOST', 'localhost'))}})

producer = KafkaProducer(bootstrap_servers=os.getenv('KAFKA_HOST'))

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
    url = urljoin(app.config['IMAGE_URL'], os.path.basename(filepath))
    producer.send('image', url.encode('utf-8'))
    return url

if __name__ == '__main__':
    app.debug = os.getenv(ENV_FORMAT.format('DEBUG'), 'DEBUG') == 'DEBUG'
    app.run(host=os.getenv(ENV_FORMAT.format('HOST'), '0.0.0.0'),
            port=int(os.getenv(ENV_FORMAT.format('PORT'), 3000)))
