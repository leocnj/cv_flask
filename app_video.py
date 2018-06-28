#
# based on https://stackoverflow.com/questions/11262518/how-to-pass-uploaded-image-to-template-html-in-flask
# - simple form to upload images
# - redirect to uploaded_file to show image
#
#
import os
from subprocess import call

from flask import Flask, render_template, request, send_from_directory, redirect, url_for
import base64
import logging

app = Flask(__name__)

UPLOAD_FOLDER = os.path.basename('uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

PROCESSED_FOLDER = os.path.basename('processed')
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER
app.debug = True

@app.route('/')
def hello_world():
    return render_template('home_video.html')


@app.route('/webrtc')
def record_webrtc():
    return render_template('webrtc.html')

# use redirect based on http://bit.ly/2KwDMlB
@app.route('/rtc_result')
def rtc_result():
    return render_template('base64.html')


@app.route('/from_rtc', methods=['POST'])
def upload_base64():
    file = request.values['fileData']
    starter = file.find(',')
    image_data = file[starter+1:]
    image_data = bytes(image_data, encoding="ascii")
    with open('uploads/base64.jpeg', 'wb') as fh:
        fh.write(base64.decodebytes(image_data))
    filename = 'base64.jpeg'
    run_openface(filename)
    # redirect doesn't work for POST not from browser
    # processed_img = filename.replace('jpeg', 'jpg')
    return redirect(url_for('rtc_result'))


@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['video']
    filename = file.filename
    f = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(f)
    run_openface(filename)
    processed_img = filename # always use mp4
    return render_template('home_video.html', img_org=filename, img_proc=processed_img)


def run_openface(filename):
    '''

    :param filename:
    :return:
    '''
    with open("./tmp/output.log", 'a') as output:
        call(
            "/opt/OpenFace/build/bin/FeatureExtraction -f " + os.path.join(app.config['UPLOAD_FOLDER'], filename),
            shell=True, stdout=output, stderr=output)
        # need convert avi to mp4 for display
        avi = filename.replace('mp4', 'avi')
        print("convert {} to {}".format(avi, filename))
        call(
            "ffmpeg -i " + os.path.join(app.config['PROCESSED_FOLDER'], avi) + " -y " + os.path.join(app.config['PROCESSED_FOLDER'], filename),
            shell=True, stdout=output, stderr=output)


# need this for showing images
@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route('/processed/<filename>')
def send_file2(filename):
    return send_from_directory(PROCESSED_FOLDER, filename)


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, host='0.0.0.0')