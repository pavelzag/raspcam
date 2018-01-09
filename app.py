import os
import picamera
from bottle import Bottle, run, static_file, route, BaseRequest

app = Bottle()
BaseRequest.MEMFILE_MAX = 1000000
camera = picamera.PiCamera()


# @get('/get_image')
# def get_image():
#     camera.capture('image.jpg')
#     return send_file(filename, mimetype='image/gif')

@route('/image')
def video_image():
    camera.capture("image.jpg", format='jpeg')

    return static_file("image.jpg",
                       root=".",
                       mimetype='image/jpg')

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    run(debug=True, host='0.0.0.0', port=port, reloadable=True)