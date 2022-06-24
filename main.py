import os
import re
from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
import zipfile
import shutil
from konlpy.tag import Mecab

from collections import Counter

from wordcloud import WordCloud

import torch

from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import TextClassificationPipeline
# -*- coding: utf-8 -*-


"""라이브러리 불러오기"""

import pandas as pd
import numpy as np

#Thread 생성을 위한 라이브러리

from threading import Thread


print("서버 설정을 시작합니다.")



os.environ["TOKENIZERS_PARALLELISM"] = "false"

#모델 불러오기
print("모델과 토크나이저를 불러옵니다.")
tokenizer = AutoTokenizer.from_pretrained("powerwarez/kindword-klue_bert-base")

model = AutoModelForSequenceClassification.from_pretrained("powerwarez/kindword-klue_bert-base")

#GPU 설정
#device = torch.device("cuda:0")
device = torch.device("cpu")


# Mecab 사용
mecab = Mecab()

#불용어 정의
stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다']

#Classification Pipe 설정
pipe = TextClassificationPipeline(model=model, tokenizer=tokenizer, return_all_scores=True)

orig_path = os.getcwd()
upload_f = orig_path+'/uploads/'
app = Flask(__name__)
app.config['upload_f'] = upload_f
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

wrong_sentences = []
komoNV = []
test_acc = 86

p = re.compile(r'\d{4}. \d{1,2}. \d{1,2}. \w{2} \d{1,2}:\d{1,2}, (.*) : (.*)')
k = re.compile('[ㄱ,ㄲ,ㄴ,ㄷ,ㄸ,ㄹ,ㅁ,ㅂ,ㅃ,ㅅ,ㅆ,ㅇ,ㅈ,ㅉ,ㅊ,ㅋ,ㅌ,ㅍ,ㅎ,ㅏ,ㅑ,ㅓ,ㅕ,ㅗ,ㅛ,ㅜ,ㅠ,ㅡ,ㅣ]+')

print("서버 설정이 완료되었습니다.")

# 업로드 HTML 렌더링
@app.route('/')
def render_file():
  global wrong_sentences
  global komoNV
  wrong_sentences = []
  komoNV = []
  if os.path.isdir(upload_f):
    shutil.rmtree(upload_f)
  os.mkdir(upload_f)

  return render_template('home.html')

# 파일 업로드 처리
@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file_path = os.path.join(upload_f, filename)
        file.save(file_path)
        unzip_file_names = []
        if filename[-3:] == "txt": #안드로이드용
          unzip_file_names.append(filename)
          print(unzip_file_names)
        elif filename[-3:] == "zip": #IOS용
          myzip_r = zipfile.ZipFile(file_path, 'r')
          unzip_file_names = myzip_r.namelist()
          myzip_r.extractall(upload_f)
          myzip_r.close()
        
        user_list = []
        
        for unzip_filename in unzip_file_names:
          unzip_filename = upload_f + unzip_filename
          with open(unzip_filename,"r",encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
              match_p = p.match(line)
              if match_p:
                retouch_user = re.sub(" : .*", "", match_p.group(1))
                if retouch_user not in user_list:
                    user_list.append(retouch_user)

        return render_template('username.html', user_list = user_list, count_user = len(user_list))

@app.route('/prediction', methods = ['GET', 'POST'])
def prediction():
  try:
    def fc_predict_score(sentence):
        value = pipe(sentence)
        print(f'{sentence}결과는 {value}')
        return value[0]     
    def make_wordcloud(sentence): #Mecab용 워드클라우드 함수
      for word in mecab.nouns(sentence):
        print(f"word는{word}")
        komoNV.append(word)
    def score_pre(line):
        global wrong_sentences
        match_p = p.match(line)
        #print('score_pre가 실행되었습니다.')
        if match_p:
          if match_p.group(1) == username:
            print(f'예측할 내용은: {match_p.group(2)}')
            make_wordcloud(match_p.group(2))
            try:
              
              sentence_li = []
              sentence_li.append(match_p.group(2))
              predict_score = fc_predict_score(sentence_li)
              # print(f"predict_score는 {predict_score}")
              # print(f"predict_score[0]는 {predict_score[0]}")
              # print(f"predict_score[0]['score']는 {predict_score[0]['score']}")
              # print(f"predict_score[1]['score']는 {predict_score[1]['score']}")
              if predict_score[0]['score']< predict_score[1]['score']:
                wrong_sentences.append(match_p.group(2))
                result = predict_score[1]['score']
                #print(f"result 는 {result}")
                return result
            except:
              pass  
        else:
          pass  
    def consonant_find(line):
        match_p = p.match(line)
        if match_p:
          if match_p.group(1) == username:
            if k.search(match_p.group(2)):
              if k.search(match_p.group(2)) != None:
                return 1
          else:
            pass
        else:
          pass
    def countLine(line):
        match_p = p.match(line)
        if match_p:
          if match_p.group(1) == username:
            return 1
          else:
            pass
        else:
          pass
    
    username = request.args.get("username")
    count_lines = 0
    consonant = 0
    score = 0
    kindword_percent = 0
    consonant_percent = 0

    if request.method == 'GET':
      os.chdir(upload_f)
      #try:
      txtfile_list = os.listdir()
      for file_text in txtfile_list:
        if file_text[-3:] != "zip":
          with open(file_text,"r",encoding='utf-8') as f:
              lines = f.readlines()
              score_list = list(map(lambda line : score_pre(line), lines))
              score = sum(list(filter(None, score_list)))
              consonant = list(map(lambda line : consonant_find(line), lines))
              consonant = sum(list(filter(None, consonant)))
              count_lines = list(map(lambda line : countLine(line), lines))
              count_lines = sum(list(filter(None, count_lines)))
              kindword_score = count_lines - score
              print(f'score:{score}, consonant:{consonant}, count_lines:{count_lines}')
      print(f"score:{score}, consonant:{consonant}, count_lines:{count_lines}")
      
      if score == 0:
        kindword_percent = 100
      else:
        kindword_percent = round(100-(score/count_lines * 100), 2)
      
      if consonant == 0:
        consonant_percent = 0
      else:
        consonant_percent = round(consonant/count_lines * 100, 2)
        
  except:
    return redirect("/")
    
  # 업로드 폴더 삭제
  shutil.rmtree(upload_f)
  os.mkdir(upload_f)
  os.chdir(orig_path)

  # Wordcloud 만들기
  counts = Counter(komoNV)
  tags = counts.most_common(100)

  if len(tags)>0:
    wc = WordCloud(font_path = orig_path+"/data/font/NotoSansKR-Black.otf",background_color="white", max_font_size=200)
    cloud = wc.generate_from_frequencies(dict(tags))
    # 생성된 WordCloud 저장
    cloud.to_file(orig_path+'/static/images/wordcloud.jpg')
    print('word cloud가 저장되었습니다.')
  else:
    pass

  return render_template('result.html', 
                          count_lines = count_lines, 
                          kindword_score = kindword_score, 
                          kindword_percent=kindword_percent, 
                          consonant_percent = consonant_percent, 
                          consonant = consonant, 
                          test_acc = test_acc, 
                          wrong_sentences=wrong_sentences)

if __name__ == '__main__':
    # 서버 실행
    app.run(host="0.0.0.0", threaded = True)