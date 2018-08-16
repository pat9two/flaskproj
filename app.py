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

    with zipfile.ZipFile(APP_ROOT + '/photos/' + request.form['id'] + '.zip', 'w', zipfile.ZIP_DEFLATED) as myzip:
        for file in request.files.getlist('file'):

            # The path to save
            temp_full_path = APP_ROOT + '/temp/' + file.filename

            # The filenames to return to the frontend
            filenames.append(file.filename)

            # Save the file to the server
            file.save(temp_full_path)

            # Write the file to the zip object
            myzip.write(temp_full_path, file.filename)

            # Delete the file from the server
            os.remove(temp_full_path)

    return render_template('success.html', filenames=filenames)


@app.route('/orders/<string:ordernum>')
def orders(ordernum):
    images_path = "".join([APP_ROOT, '/photos/'])

    if os.path.exists(images_path + ordernum + '.zip'):
        return send_file(images_path + ordernum + '.zip', 'application/zip')

    else:
        # If the user types a order number that doesn't exist return 404
        abort(404)
