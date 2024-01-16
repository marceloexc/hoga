from flask import Flask, send_from_directory, render_template, request, session
import os

app = Flask(__name__)
app.secret_key = 'hoga'

@app.route('/', methods=['GET', 'POST'])
def index():
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

if __name__ == '__main__':
    app.run(debug=True)
