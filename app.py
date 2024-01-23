import sqlite3
from flask import Flask, send_from_directory, render_template, request, session, g
import os
import database
import twitter


app = Flask(__name__)
app.secret_key = 'hoga'

# DATABASE = "test.db"
#
# def get_db():
#     db = getattr(g, '_database', None)
#     if db is None:
#         db = g._database = sqlite3.connect(DATABASE)
#     return db
#
# @app.teardown_appcontext
# def close_connection(exception):
#     db = getattr(g, '_database', None)
#     if db is not None:
#         db.close()
#
#
# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         session['image_folder'] = request.form.get('image_folder')
#     image_folder = session.get('image_folder')
#     if image_folder:
#         image_files = os.listdir(image_folder)
#         image_files = [f for f in image_files if f.endswith(('.png', '.jpg', '.jpeg', '.gif', '.mp4'))]
#         image_urls = [f'/images/{f}' for f in image_files]
#     else:
#         image_urls = []
#     return render_template('index.html', image_urls=image_urls)
#
#
# # fuck globals
# @app.route('/images/<path:filename>')
# def images(filename):
#     image_folder = session.get('image_folder')
#     return send_from_directory(image_folder, filename)

@app.route('/')
def index():
    print("Hello")
    hello = database.create_table()
    twitter_extractor = twitter.Twitter()
    metadata_files = twitter_extractor.glob_files(
        '/Users/marceloexc/gallery-dl/twitter/xe0_xeo', ['*.json']
    )
    twitter_metadata_dict = twitter_extractor.make_dict(metadata_files)
    twitter_extractor.insert_into_database(twitter_metadata_dict)
    return str(twitter_metadata_dict)





if __name__ == '__main__':
    app.run(debug=True)
