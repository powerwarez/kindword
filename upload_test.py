import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/uploads'
if not os.path.isdir(UPLOAD_FOLDER):                                                           
    os.mkdir(UPLOAD_FOLDER)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# 업로드 HTML 렌더링
@app.route('/')
def render_file():
    return render_template('home.html')

# 파일 업로드 처리
@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        
        # 저장할 경로 + 파일명
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 'uploads 디렉토리 -> 파일 업로드 성공!'

if __name__ == '__main__':
    # 서버 실행
    app.run()