from flask import Flask, render_template, request
import re
import string
import os
import nltk
import pyodbc
from nltk import stem
from nltk import word_tokenize
nltk.download('punkt')


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

@app.route('/task1', methods=['GET', 'POST'])
def nchars():
    task1list =  []
    nval = int(request.form.get('task1'))
    with open('C:/Users/16693/Desktop/adbassignment5/static/Grimm.txt', 'r', encoding="utf-8") as input:
        for line in input:
            allWords = nltk.tokenize.word_tokenize(line)
            for words in allWords:
                if words.istitle() == True:
                    task1list.append(words)
            allWordDist = nltk.FreqDist(w for w in task1list)
            mostCommon= allWordDist.most_common(nval)
            #print(mostCommon)
    return render_template('task1.html', finaldata = mostCommon, nchar=nval)

if __name__ == '__main__':
    app.run(debug=True)