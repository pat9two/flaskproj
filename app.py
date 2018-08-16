import os
from flask import Flask, render_template, request, url_for, send_from_directory, send_file, abort
import zipfile

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():

    filenames=[]
    for file in os.listdir(APP_ROOT + '/temp'):
        os.remove(APP_ROOT +'/temp/' + file)

    with zipfile.ZipFile(APP_ROOT + '/photos/' + request.form['id'] + '.zip', 'w') as myzip:
        for file in request.files.getlist('file'):
            filenames.append(file.filename)
            file.save(APP_ROOT + '/temp/ ' + file.filename)

        for name in filenames:
            myzip.write(APP_ROOT + '/temp/ ' + name, name)

            if os.path.exists(APP_ROOT + '/temp' + name):
                os.remove(APP_ROOT + '/temp/' + name)

    return render_template('success.html', filenames=filenames)


@app.route('/orders/<string:ordernum>')
def orders(ordernum):
    print(APP_ROOT)
    images_path = "".join([APP_ROOT, '/photos/'])

    if os.path.exists(images_path + ordernum + '.zip'):

        return send_file(images_path + ordernum + '.zip', 'application/zip')

    else:
        abort(404)
