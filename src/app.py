import os

from flask import Flask, send_from_directory, render_template, request, session
import database
import json
import twitter
from ast import literal_eval

app = Flask(__name__)
app.secret_key = 'hoga'
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
EXTENSIONS = ['*.json']
MEDIA_EXTENSIONS = ['*.jpg', '*.png', '*.mp4', '*.jpeg']



@app.route('/home', methods=['GET', 'POST'])
def get():
    if request.method == 'POST':
        session['image_folder'] = request.form.get('image_folder')
    image_folder = session.get('image_folder')
    if image_folder:
        image_files = os.listdir(image_folder)
        image_files = [f for f in image_files if f.endswith(('.png', '.jpg', '.jpeg', '.gif', '.mp4'))]
        image_urls = [f'/images/{f}' for f in image_files]
    else:
        image_urls = []
    return render_template('index.html', image_urls=image_urls)


# fuck globals
@app.route('/images/<path:filename>')
def images(filename):
    image_folder = session.get('image_folder')
    return send_from_directory(image_folder, filename)


@app.route('/')
def index():
    hello = database.create_table()
    twitter_extractor = twitter.Twitter()
    metadata_files = twitter_extractor.glob_files(
        '/Users/marceloexc/gallery-dl/twitter/xe0_xeo', ['*.json']
    )
    twitter_extractor.json_run(metadata_files, '/Users/marceloexc/gallery-dl/twitter/xe0_xeo')
    # return "hello"


    with app.app_context():
        db = database.get_db()
        cur = db.cursor()
        cur.execute('SELECT * FROM metadata_table')
        results = cur.fetchall()

    results_dicts = []
    for result in results:
        result_dict = {
            'identifier': result[0],
            'metadata_file_path': result[1],
            'media_files': literal_eval(result[2]),
            'date': result[3]
        }
        results_dicts.append(result_dict)

    return render_template('index test.html', results=results_dicts)



# Define a custom 404 error handler
@app.errorhandler(404)
def page_not_found(e):
    # Render a custom template for the 404 error page
    return render_template('404.html'), 404
@app.route("/hello")
def hello404():
    return render_template('home.html')

# TODO: remove this

def read_file(file_path):
    with open(file_path, 'r') as w:
        data = json.load(w)
        print(data)
        return json.dumps(data, indent=4,  separators=(',', ':'))

app.jinja_env.globals.update(read_file=read_file)


if __name__ == '__main__':
    app.run(debug=True)
