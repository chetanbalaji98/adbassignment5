from flask import Flask, render_template, request, jsonify
import re
import string
import os
import nltk
import pyodbc
from collections import Counter 
from nltk import stem
from nltk import word_tokenize
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')


application = app = Flask(__name__)
app.secret_key = "Secret Key"

app = Flask(__name__)
app.config["image_folder"] = "./static/"
app.config['UPLOAD_EXTENSIONS'] = ['jpg', 'png', 'gif']
app.secret_key = "Secret Key"


DRIVER = '{ODBC Driver 18 for SQL Server}'
SERVER = 'adbserver.database.windows.net'
DATABASE = 'chetanadb'
USERNAME = 'chetanbalaji'
PASSWORD = 'Springadb123'

cnxn = pyodbc.connect("Driver={};Server=tcp:{},1433;Database={};Uid={};Pwd={};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;".format(DRIVER, SERVER, DATABASE, USERNAME, PASSWORD))
crsr = cnxn.cursor()

conn = pyodbc.connect("Driver={};Server=tcp:{},1433;Database={};Uid={};Pwd={};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;".format(DRIVER, SERVER, DATABASE, USERNAME, PASSWORD))
cursor = conn.cursor()


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

# @app.route('/task1', methods=['GET', 'POST'])
# def nchars():
#     task1list =  []
#     nval = int(request.form.get('task1'))
#     with open('static/Grimm.txt', 'r', encoding="utf-8") as input:
#         for line in input:
#             allWords = nltk.tokenize.word_tokenize(line)
#             for words in allWords:
#                 if words.istitle() == True:
#                     task1list.append(words)
#             allWordDist = nltk.FreqDist(w for w in task1list)
#             mostCommon= allWordDist.most_common(nval)
#             #print(mostCommon)
#     return render_template('task1.html', finaldata = mostCommon, nchar=nval)

@app.route('/task1', methods=['GET', 'POST'])
def get_top_nouns():
    nval = int(request.form.get('task1'))
    with open("C://Users//16693//Desktop//adbassignment5//static//Grimm.txt", 'r', encoding="utf-8") as file:
        story = file.read()
    tokens = nltk.word_tokenize(story)
    pos_tags = nltk.pos_tag(tokens)
    nouns = [word.lower() for word, tag in pos_tags if word[0].isupper()]
    noun_counts = Counter(nouns)
    top_nouns = noun_counts.most_common(nval)
    
    print(top_nouns)
    return render_template('task1.html', finaldata = top_nouns, nchar=nval)

# @app.route('/task2', methods=['GET', 'POST'])
# def searchword():
#     searching = []
#     countoccur =[]
#     charclist = []
#     percentlist = []
#     searchword  = request.form.get('task2')
#     for word in searchword:
#         for charc in word.split():
#             charclist.append(charc)
#             with open("C://Users//16693//Desktop//adbassignment5//static//Grimm.txt", 'r', encoding="utf-8") as input:
#                 for line in input:
#                     for word in line:
#                         for charct in word:
#                             if charct == charc:
#                                 searching.append(charct)
#     for i in range(len(charclist)):
#         pwoe = searching.count(charclist[i])
#         countoccur.append(pwoe)
#     file = open("C://Users//16693//Desktop//adbassignment5//static//Grimm.txt", 'r', encoding="utf-8")
#     data = file.read().replace(" ","")
#     number_of_characters = len(data)
#     print(number_of_characters)
#     for i in range(len(countoccur)):
#         print(countoccur[i])
#         percenttotal = (countoccur[i] / number_of_characters )*100
#         percentlist.append(percenttotal)
#     print(percentlist)
#     finaldata = list(zip(charclist, countoccur, percentlist))
#     print(finaldata)
#     return render_template('task2.html', finaldata=finaldata,)


@app.route('/task2', methods=['GET', 'POST'])
def get_character_stats():

    word  = request.form.get('task2')
    with open("C://Users//16693//Desktop//adbassignment5//static//Grimm.txt", 'r', encoding="utf-8") as file:
        text = file.read()
    count_dict = {char: text.count(char) for char in word}
    total_chars = len(text)
    results = []
    for char in word:
        count = count_dict[char]
        percent = round((count / total_chars) * 100, 2)
        results.append((char, count, percent))
    return render_template('task2.html', finaldata=results,)


@app.route('/practice1', methods=['GET', 'POST'])
def practice1():
    search_word=request.form.get('search')
    result = []
    with open("C://Users//16693//Desktop//adbassignment5//static//Grimm.txt", 'r', encoding="utf-8") as f:
        for i, line in enumerate(f):
            if search_word.lower().strip() in line.lower().strip():
                result.append((i+1, line.strip()))
    if not result:
        result.append(("No results found for search word: " + search_word,))

    print(result)
    return render_template('practice1.html', finaldata=result,)

if __name__ == '__main__':
    app.run(debug=True)