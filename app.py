import os
import platform
import socket
from logger import logging_handler
from configuration import get_owner
from bottle import Bottle, run, static_file, route, BaseRequest, template
from PIL import Image
from send_mail import send_mail
from GoogleOCR import detect_text

creds_path = os.path.join(os.getcwd(), "googlecreds.json")
owner = get_owner
logging_handler(creds_path)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = creds_path
logging_handler(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])
app = Bottle()
BaseRequest.MEMFILE_MAX = 1000000
image_file = "image.jpeg"
post_crop = "image_post_crop.jpeg"
local_envs = ['Darwin', 'fedora']
current_platform = platform.platform()
msg = '{} {}'.format('Current platform is:', current_platform)
logging_handler(msg)


def capture():
    import picamera
    camera = picamera.PiCamera()
    print('capturing the image')
    camera.capture(image_file, format='jpeg')
    camera.close()


def image_crop():
    print('cropping the image')
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


def get_machine_ip():
    """Gets the running machine's IP address"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

@route('/')
def index():
    if not any(env in current_platform for env in local_envs):
        capture()
        image_crop()
    whole = detect_text(post_crop)
    info = {'content': whole}
    return template('index.tpl', info)


@route('/get_image')
def get_image():
    if not any(env in current_platform for env in local_envs):
        capture()
        image_crop()
    return static_file(post_crop,
                       root=".",
                       mimetype='image/jpg')


@route('/get_full_image')
def get_full_image():
    if not any(env in current_platform for env in local_envs):
        capture()
        image_crop()
    return static_file(image_file,
                       root=".",
                       mimetype='image/jpg')


@route('/static/<filename>')
def server_static(filename):
    return static_file(post_crop, root='')


if __name__ == "__main__":
    ip_address = get_machine_ip()
    startup_msg = '{} {}'.format('Rasp Cam machine runs on', ip_address)
    send_mail(send_to=owner, subject='Start up Message', text=startup_msg)
    port = int(os.environ.get('PORT', 8081))
    run(debug=True, host='0.0.0.0', port=port, reloadable=True)