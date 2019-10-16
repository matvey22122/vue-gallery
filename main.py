import os
import random
import string
from flask import *
from PIL import Image
import requests
from io import BytesIO
import math


class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        variable_start_string='%%',  # Default is '{{', I'm changing this because Vue.js uses '{{' / '}}'
        variable_end_string='%%',
    ))


app = CustomFlask(__name__,
                  static_folder='dist/',
                  template_folder='dist/')

app.config["SRC"] = 'dist/static/src'
app.config["THUMBNAIL"] = 'dist/static/thumbnail'


def id_generator(size=12, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def resize_image(input_image_path,
                 output_image_path):
    original_image = Image.open(input_image_path)
    width, height = original_image.size
    if width < height:
        new_size = (200, round(200 / width * height))
    else:
        new_size = (round(200 / height * width), 200)
    resized_image = original_image.resize(new_size)
    width, height = resized_image.size
    new_width = 200
    new_height = 200
    left = (width - new_width) / 2
    top = (height - new_height) / 2
    right = (width + new_width) / 2
    bottom = (height + new_height) / 2
    area = (left, top, right, bottom)
    resized_image = resized_image.crop(area)
    resized_image.save(output_image_path)


def size_image(input_image_path):
    original_image = Image.open(input_image_path)
    return original_image.size


@app.route('/get_images')
def get_images():
    name_of_images = []
    for file in os.listdir('dist/static/src/'):
        name_of_images.append(file)
    return json.dumps(name_of_images)


@app.route('/get_src/<filename>')
def get_src(filename):
    return send_from_directory(app.config['SRC'], filename=filename)


@app.route('/get_w/<filename>')
def get_w(filename):
    return json.dumps((size_image('dist/static/src/'+filename))[0])


@app.route('/get_h/<filename>')
def get_h(filename):
    return json.dumps((size_image('dist/static/src/'+filename))[1])


@app.route('/get_thumbnail/<filename>')
def get_thumbnail(filename):
    return send_from_directory(app.config['THUMBNAIL'], filename=filename)


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        for i in request.files.getlist('IMAGES'):
            filename = id_generator() + '.' + i.filename.split('.')[1]
            i.save(os.path.join('dist/static/src', filename))
            resize_image('dist/static/src/'+filename, 'dist/static/thumbnail/'+filename)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
