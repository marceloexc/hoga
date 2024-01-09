from flask import Flask, render_template, request, make_response, send_file, send_from_directory
from twitter import Twitter
import os

app = Flask(__name__)


# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         # Get the value entered in the text field
#         user_input = request.form['user_input']
#         json_files = Twitter.retrieve_files(user_input)
#         for key, value in json_files.items():
#             print(key, value)
#         user_input = json_files
#         return render_template('index.html', user_input=user_input)
#     return render_template('index.html', user_input=None)
# Main route to render a template that displays all images


# Function to get a list of all image filenames in the 'images' folder
def get_image_filenames(folder_path):
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif']  # Add more extensions as needed
    image_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f.lower().endswith(tuple(image_extensions))]
    return image_files


# Main route to render a template that displays all images
@app.route('/')
def index():
    # Assuming the 'images' folder is in the parent directory of the Flask app
    images_folder_path = os.path.join(os.path.dirname(__file__), '..', 'images')

    # Get a list of all image filenames in the 'images' folder
    image_filenames = get_image_filenames(images_folder_path)

    return render_template('index.html', image_filenames=image_filenames)


@app.route('/images/<filename>')
def display_image(filename):
    return send_from_directory('../images', filename)


if __name__ == '__main__':
    app.run(debug=True)
