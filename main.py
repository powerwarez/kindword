import sentiment_predict
from flask import Flask, render_template, request

from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences



UPLOAD_FOLDER = './uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# 업로드 HTML 렌더링
@app.route('/')
def render_file():
  return render_template('home.html')

# 파일 업로드 처리
@app.route('/read')
def read():
  word = request.args.get("word")
  result = sentiment_predict(word)
  return render_template("report.html", result=result)



if __name__ == '__main__':
    # 서버 실행
    app.run(host="0.0.0.0")