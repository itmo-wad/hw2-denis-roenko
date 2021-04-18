from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/img/<int:image_id>')
def get_image(image_id):
    return send_from_directory('static\\img', f'image{image_id}.jpg')

@app.route('/static/<path:filename>')
def get_static_file(filename):
    return app.send_static_file(filename)

if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)