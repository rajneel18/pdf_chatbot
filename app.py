# from flask import Flask, render_template, request, jsonify
# from pdf_processor import process_pdf, answer_question
# import os

# if not os.path.exists('uploads'):
#     os.makedirs('uploads')

# app = Flask(__name__)

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         if 'file' not in request.files:
#             return jsonify({'error': 'No file part'})
#         file = request.files['file']
#         if file.filename == '':
#             return jsonify({'error': 'No selected file'})
#         if file and file.filename.endswith('.pdf'):
#             filename = file.filename
#             file.save(os.path.join('uploads', filename))
#             chunks = process_pdf(os.path.join('uploads', filename))
#             return render_template('result.html', filename=filename)
#     return render_template('index.html')

# @app.route('/ask', methods=['POST'])
# def ask():
#     question = request.form['question']
#     filename = request.form['filename']
#     answer = answer_question(question, filename)
#     return jsonify({'answer': answer})

# if __name__ == '__main__':
#     app.run(debug=True)

# @app.route('/', methods=['GET'])
# def home():
#     return "Hello from Vercel!"

# if __name__ == '__main__':
#     app.run()



# from flask import Flask, render_template, request, jsonify
# from pdf_processor import process_pdf, answer_question
# import os

# # if not os.path.exists('uploads'):
# #     os.makedirs('uploads')

# app = Flask(__name__)

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         if 'file' not in request.files:
#             return jsonify({'error': 'No file part'})
#         file = request.files['file']
#         if file.filename == '':
#             return jsonify({'error': 'No selected file'})
#         if file and file.filename.endswith('.pdf'):
#             filename = file.filename
#             file.save(os.path.join('uploads', filename))
#             chunks = process_pdf(os.path.join('uploads', filename))
#             return render_template('result.html', filename=filename)
#     return render_template('index.html')

# @app.route('/ask', methods=['POST'])
# def ask():
#     question = request.form['question']
#     filename = request.form['filename']
#     answer = answer_question(question, filename)
#     return jsonify({'answer': answer})

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from io import BytesIO
import os

app = Flask(__name__)

# Remove the line that creates the 'uploads' directory
# os.makedirs('uploads')  # This line should be removed

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Instead of saving to disk, process in memory
        file_content = file.read()
        # Here you can process the file_content as needed
        # For example, you could print the size:
        print(f"Received file '{filename}' of size {len(file_content)} bytes")
        
        # If you need to do something with the file content, do it here
        # For example, you could return the file size
        return jsonify({'message': 'File uploaded successfully', 'size': len(file_content)}), 200
    return jsonify({'error': 'File type not allowed'}), 400

if __name__ == '__main__':
    app.run(debug=True)