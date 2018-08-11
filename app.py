import os
from flask import Flask, render_template, request, url_for, send_from_directory

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    target = os.path.join(APP_ROOT, request.form['id'] + '/')
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)
    filenames = []
    for file in request.files.getlist('file'):
        print(file)
        filename = file.filename
        destination = "".join([target, filename])
        filenames.append(filename)
        file.save(destination)
    return render_template('success.html', filenames=filenames)


@app.route('/orders/<string:ordernum>')
def orders(ordernum):
    images_path = "".join([APP_ROOT, '/', ordernum, '/'])

    print(images_path)
    return send_from_directory(images_path, '*')
