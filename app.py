import os
import picamera
# from bottle import Bottle, run, get, BaseRequest
from flask import Flask,send_file

filename = 'image.jpg'
app = Flask(__name__)
# BaseRequest.MEMFILE_MAX = 1000000
camera = picamera.PiCamera()


@app.route('/get_image')
def get_image():
    camera.capture(filename)
    return send_file(filename, mimetype='image/gif')

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, use_reloader=True)
