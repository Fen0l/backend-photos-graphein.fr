import time
import requests, os, sys, datetime, base64

from flask import Flask, render_template, request, jsonify, send_from_directory, url_for
from jinja2 import Environment, FileSystemLoader
from werkzeug import secure_filename

from logging import Formatter, FileHandler

from PIL import Image

from GithubManager import GithubWorker

basedir = os.path.abspath(os.path.dirname(__file__))


# Flask settings
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg'])
app.jinja_env.cache = {}
app.config['WORKING_GIT_DIRECTORY'] = os.getcwd() + '/tmp/'


# jinja2 settings
PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_ENVIRONMENT = Environment(
    autoescape=False, 
    loader=FileSystemLoader(os.path.join(PATH, 'templates')), 
    trim_blocks=False
)


# Logging setup
handler = FileHandler(os.path.join(basedir, 'log.txt'), encoding='utf8')
handler.setFormatter(
    Formatter("[%(asctime)s] %(levelname)-8s %(message)s", "%Y-%m-%d %H:%M:%S")
)
app.logger.addHandler(handler)



# Github settings
gw = GithubWorker()
local_folders = gw.get_folders()



# def _check_img_filename(filename):
#     print("CHECKING " + filename)
#     if(os.path.isfile(local_folders['picture'] + filename)):
#         filename_structure = filename.split(".")

#         occuration = filename_structure[0].split("-")
#         occuration = int(occuration[1]) if(len(occuration) > 1) else 0

#         filename = "{o_filename}-{number}.{ext}".format(
#             ext = filename_structure[-1], 
#             o_filename = filename_structure[0].split('-')[0], 
#             number = occuration + 1
#             )

#         return _check_img_filename(filename)

#     return filename

def _check_markdown_filename(filename):
    print("CHECKING " + filename)
    if(os.path.isfile(local_folders['markdown'] + filename)):
        current_filename, ext = filename.split(".")

        # Get occurative indice
        # 2017-11-13-fontaine-1.markdown


        occuration = filename_structure[0].split("-")
        occuration = int(occuration[1]) if(len(occuration) > 1) else 0

        filename = "{o_filename}-{number}.{ext}".format(
            ext = filename_structure[-1], 
            o_filename = filename_structure[0].split('-')[0], 
            number = occuration + 1
            )

        return _check_markdown_filename(filename)

    return filename



#print("test " + _check_img_filename("test.jpg"))

print("test " + _check_markdown_filename("2017-11-13-fontaine.markdown"))



# Find the template
def _render_template(template_filename, context):
    return TEMPLATE_ENVIRONMENT.get_template(template_filename).render(context)
 
# Render the empty template
def _create_template(template_filename, template_renderer):
    with open("tmp/" + template_filename, "w") as f:
        f.write(template_renderer)

def proceed_post(filename, dataForm):
    current_datetime = datetime.datetime.now()

    datas = {
        'title_photo': dataForm['title-photo'].title(),
        'img_local_name': filename,
        'description_short': dataForm['desc-photo'].split('.')[0] + ".",
        'description_long': dataForm['desc-photo'],
        'date_post': current_datetime.strftime("%Y-%m-%d %H:%M:%S"),
        'tags': dataForm['tags-photo']
    }


    # Create markdown file -> 2017-10-24-bordeaux-mirror.markdown 
    template_filename = current_datetime.strftime("%Y-%m-%d-") + datas['title_photo'].lower().replace(' ', '-') + ".markdown"
    template_renderer = _render_template('empty_template.markdown', datas)
    _create_template(template_filename, template_renderer)

    # commit_gh(["tmp/" + template_filename, "tmp/" + filename])

    _init_local_repo()


# Check if the file match with the settings
def _allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# HTTP GET /
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/uploadajax', methods=['POST'])
def upldfile():
    if request.method == 'POST':
        files = request.files.getlist('file')
        for f in files:
            f.filename = f.filename.lower()
            if f and _allowed_file(f.filename):
                filename = secure_filename(f.filename)
                updir = os.path.join(basedir, app.config['WORKING_GIT_DIRECTORY'])
                print("UPDIR " + updir)

                # CHeck if file exists and rename it if yes
                filename = _check_img_filename(filename)

                f.save(os.path.join(updir, filename))
                file_size = os.path.getsize(os.path.join(updir, filename))
                proceed_post(filename, request.form)
            else:
                app.logger.info('ext name error')
                return jsonify(error='ext name error')

        return jsonify(name=filename, size=file_size, status="posted")


if __name__ == '__main__':
    app.run(use_reloader=True, debug=True)
