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


@app.route('/cbd10a', methods=['POST'])
def cbd10a():
    text = request.form['t']
    n = len(text)
    u = sum(1 for c in text if c.isupper())
    p = sum(1 for c in text if c.isspace())
    c = sum(1 for c in text if c in '.,:?$()-&')
    v = sum(1 for c in text if c.isnumeric())
    print(n)
    print(u)
    result = f"N = {n}\nU = {u}\nP = {p}\nC = {c}\nV = {v}"
    return render_template('cbd10a.html', n=n, u=u, p=p, c=c, v=v, text=text,result=result)


@app.route('/cbd10b', methods=['GET', 'POST'])
def tenb():
    if request.method == 'POST':
        text = ''
        result = ''
        count = 0
        if request.method == 'POST':
            text = request.form['t']
            # remove punctuation and numbers, change to uppercase
            result = ''.join(c for c in text if c.isalpha() or c.isspace()).upper()
            count = len(result)
        results=f"N = {result}\nU = {count}"
        return render_template('cbd10b.html',filter='10b', text=text, result=result, count=count)





def count_words(text, words):
    text = ''.join(c for c in text if c.isalnum() or c.isspace())
    word_list = words.split()
    count = {word: text.lower().count(word.lower()) for word in word_list}
    return count

@app.route('/cbd11a', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        box_s = request.form['S']
        box_t = request.form['T']
        result = count_words(box_t, box_s)
        
        resulta=str(result)
        results=f"N = {resulta}"
    print(results)
    return render_template('cbd11a.html',results=results)


def count_word_pairs(text, word_pair):
    # remove punctuation and digits, and split into words
    words = text.translate(str.maketrans('', '', string.punctuation + string.digits)).split()
    word1, word2 = word_pair.split()
    print(words)
    word_count = 0
    word_locations = []
    # iterate over the words in the text to find adjacent pairs
    for i in range(len(words)-1):
        if (words[i] == word1 and words[i+1] == word2) or (words[i] == word2 and words[i+1] == word1):
            word_count += 1
            word_locations.append(i)
    return word_count, word_locations

@app.route('/cbd11b', methods=['GET', 'POST'])
def cbd11b():
    if request.method == 'POST':
        text = request.form['S']
        text1 = text
        word_pair = request.form['T']
        word_pair1 = word_pair
        if len(word_pair.split()) != 2:
            error_msg = 'Please enter only two words separated by a space in the second text box.'
            return render_template('error.html', error_msg=error_msg)
        text = text.upper().translate(str.maketrans('', '', string.punctuation + string.digits))
        word_pair = word_pair.upper().translate(str.maketrans('', '', string.punctuation + string.digits))
        word_count, word_locations = count_word_pairs(text, word_pair)
        result = f"Number of occurrences of word pair '{word_pair1}': {word_count}\nLocations: {word_locations}"
        return render_template('cbd11b.html', filter='11b', text1=text1, word_pair1=word_pair1, result=result)


    
    
    












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
    with open("static/Grimm.txt", 'r', encoding="utf-8") as file:
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
    with open("static/Grimm.txt", 'r', encoding="utf-8") as file:
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
    with open("static/Grimm.txt", 'r', encoding="utf-8") as f:
        for i, line in enumerate(f):
            if search_word.lower().strip() in line.lower().strip():
                result.append((i+1, line.strip()))
    if not result:
        result.append(("No results found for search word: " + search_word,))

    print(result)
    return render_template('practice1.html', finaldata=result,)

if __name__ == '__main__':
    app.run(debug=True)