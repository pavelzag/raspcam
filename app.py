import os
import picamera
from bottle import Bottle, run, static_file, route, BaseRequest
from PIL import Image

app = Bottle()
BaseRequest.MEMFILE_MAX = 1000000
camera = picamera.PiCamera()
image_file = "image.jpeg"
post_crop = "image_post_crop.jpeg"


def image_crop():
    img = Image.open(image_file)
    half_the_width = img.size[0] / 2
    half_the_height = img.size[1] / 2
    img4 = img.crop(
        (
            half_the_width - 150,
            half_the_height - 75,
            half_the_width + 40,
            half_the_height + 75
        )
    )
    img4.save(post_crop)


@route('/get_image')
def get_image():
    camera.capture(image_file, format='jpeg')
    image_crop()
    return static_file(post_crop,
                       root=".",
                       mimetype='image/jpg')

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8081))
    run(debug=True, host='0.0.0.0', port=port, reloadable=True)