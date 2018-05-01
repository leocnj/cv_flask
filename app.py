#
# based on https://stackoverflow.com/questions/11262518/how-to-pass-uploaded-image-to-template-html-in-flask
# - simple form to upload images
# - redirect to uploaded_file to show image
#
#
import os
from subprocess import call

from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__)

UPLOAD_FOLDER = os.path.basename('uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

PROCESSED_FOLDER = 'uploads/processed'
print(PROCESSED_FOLDER)

app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER
app.debug = True

@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['image']
    filename = file.filename
    f = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(f)
    run_openface(filename)
    processed_img = filename.replace('jpeg', 'jpg')
    return render_template('home.html', img_org=filename, img_proc=processed_img)

def run_openface(filename):
    '''

    :param filename:
    :return:
    '''
    with open("./tmp/output.log", 'a') as output:
        call(
            "docker run -v /Users/lchen/Documents/GitHub/cv_flask/uploads:/data -w \'/data\' -i -t openface_v1.0 /opt/OpenFace/build/bin/FaceLandmarkImg -f " + filename,
            shell=True, stdout=output, stderr=output)


# need this for showing images
@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route('/uploads/processed/<filename>')
def send_file2(filename):
    return send_from_directory(PROCESSED_FOLDER, filename)
