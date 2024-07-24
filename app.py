# # from flask import Flask, render_template, request, jsonify
# # from pdf_processor import process_pdf, answer_question
# # import os

# # if not os.path.exists('uploads'):
# #     os.makedirs('uploads')

# # app = Flask(__name__)

# # @app.route('/', methods=['GET', 'POST'])
# # def index():
# #     if request.method == 'POST':
# #         if 'file' not in request.files:
# #             return jsonify({'error': 'No file part'})
# #         file = request.files['file']
# #         if file.filename == '':
# #             return jsonify({'error': 'No selected file'})
# #         if file and file.filename.endswith('.pdf'):
# #             filename = file.filename
# #             file.save(os.path.join('uploads', filename))
# #             chunks = process_pdf(os.path.join('uploads', filename))
# #             return render_template('result.html', filename=filename)
# #     return render_template('index.html')

# # @app.route('/ask', methods=['POST'])
# # def ask():
# #     question = request.form['question']
# #     filename = request.form['filename']
# #     answer = answer_question(question, filename)
# #     return jsonify({'answer': answer})

# # if __name__ == '__main__':
# #     app.run(debug=True)

# # @app.route('/', methods=['GET'])
# # def home():
# #     return "Hello from Vercel!"

# # if __name__ == '__main__':
# #     app.run()



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

from flask import Flask, render_template, request, jsonify
from pdf_processor import process_pdf, answer_question
import os

UPLOAD_FOLDER = '/tmp'

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'})
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'})
        if file and file.filename.endswith('.pdf'):
            filename = file.filename
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            chunks = process_pdf(file_path)
            return render_template('result.html', filename=filename)
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    question = request.form['question']
    filename = request.form['filename']
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    answer = answer_question(question, file_path)
    return jsonify({'answer': answer})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
