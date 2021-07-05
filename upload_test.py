import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import zipfile
import re

UPLOAD_FOLDER = "C:\\Users\\User\\Desktop\\PythonWorkspace\\KindWord\\uploads\\"
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
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # 폴더 만들고 압축 풀기
        os.chdir(UPLOAD_FOLDER)
        myzip_r = zipfile.ZipFile(filename, 'r')
        if not os.path.isdir(UPLOAD_FOLDER):
            os.mkdir(filename[:-4])
        myzip_r.extractall()
        myzip_r.close()
        # uploads 폴더에서 파일 이름을 숫자로 바꾸기
        file_list = os.listdir(UPLOAD_FOLDER)
        idx_n = 1
        rename_filelist = []
        for filename in file_list:
            if filename[-3:] != "zip":
                os.rename(UPLOAD_FOLDER+filename, UPLOAD_FOLDER+str(idx_n)+'.txt')
                rename_filelist.append(UPLOAD_FOLDER+str(idx_n)+'.txt')
                idx_n += 1
        # 텍스트 파일 읽어들이기
        for filename in rename_filelist:
            path = os.path.join(UPLOAD_FOLDER, filename)
            print(path)
            with open(path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for line in lines[:1]:
                    print(line)
        #os.remove(UPLOAD_FOLDER)
           
        return 'uploads 디렉토리 -> 파일 업로드 성공!'

if __name__ == '__main__':
    # 서버 실행
    #app.run(host="0.0.0.0")
    app.run()