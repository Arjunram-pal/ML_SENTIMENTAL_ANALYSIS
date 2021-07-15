import pandas as pd
from flask import render_template, request ,url_for
#from sklearn.externals import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import classification_report
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from textblob import Word
import pickle
import joblib
import csv
import os
from werkzeug.utils import secure_filename
from flask import Flask,flash,request,redirect,send_file,render_template




from app import app

cv = CountVectorizer()

UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")
@app.route("/index")
def home():
    return render_template('home.html')


@app.route('/predict', methods=['POST'])
def predict():
    ngram_size = 1
    nb_spam_model = open("pretrainedModel/NB_model.pkl", 'rb')
    clf = joblib.load(nb_spam_model)

    dictionary_filepath = open("pretrainedModel/vocabulary_model.pkl", 'rb')
    vocabulary_to_load = joblib.load(dictionary_filepath)
    loaded_vectorizer = CountVectorizer(ngram_range=(ngram_size, ngram_size), min_df=1, vocabulary=vocabulary_to_load)
    loaded_vectorizer._validate_vocabulary()

    message = request.form['message']
    data = [message]
    vect = loaded_vectorizer.transform(data).toarray()
    my_prediction = clf.predict(vect)
    #print(my_prediction)
    return render_template('result.html', prediction=my_prediction)

"""
@app.route('/predictcsvfile', methods=[ 'GET','POST'])
def predict1():
    ngram_size = 1
    nb_spam_model = open("pretrainedModel/NB_model.pkl", 'rb')
    clf = joblib.load(nb_spam_model)

    dictionary_filepath = open("pretrainedModel/vocabulary_model.pkl", 'rb')
    vocabulary_to_load = joblib.load(dictionary_filepath)
    loaded_vectorizer = CountVectorizer(ngram_range=(ngram_size, ngram_size), min_df=1, vocabulary=vocabulary_to_load)
    loaded_vectorizer._validate_vocabulary()

    df1 = pd.read_csv("uploads/svm.csv", encoding='latin-1')
    our_list=df1['review']

    sre=[]
    for name in our_list:
        inp1 = [name]
        inp1 = loaded_vectorizer.transform(inp1).toarray()
        my_prediction1 = clf.predict(inp1)
        sre.append(my_prediction1)
        print(my_prediction1)
    
    fields = ['Sentiment'] 

    with open("predictCsv/arjun11.csv", 'w' ,newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(fields)
        writer.writerows(sre)

    return render_template('resultofcsv.html', prediction1=my_prediction1)


"""

@app.route('/uploadcsv', methods=['GET', 'POST'])
def upload_file():
    global places
    places=[]
    if request.method == 'POST':
        

        # check if the post request has the file part
        if 'file' not in request.files:
            print('no file')
            return redirect(request.url)
        file = request.files['file']
        print(file)
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
          #  print('no filename')
            return redirect(request.url)
        else:
            filename = secure_filename(file.filename)
           # print(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
           # print("saved file successfully")
      #send file name as parameter to downlad
            file_path = UPLOAD_FOLDER + filename
           # print(file_path)
            with open(file_path) as csv_file:   
                data = csv.reader(csv_file, delimiter=',')
                places= []  
                for row in data:
                    if data.line_num == 1: fields = len(row)
                    if len(row) != fields:
                        print("Number of column is not match!")
                    if fields == 1:
                        places.append({
                    "city": row[0] 
                    })
                        
                    elif fields == 2:
                        places.append({
                    "city": row[0],
                    "attraction": row[1] 
                    })
                    elif fields == 3:
                        places.append({
                    "city": row[0],
                    "attraction": row[1],
                    "attraction1": row[2] 
                    })
                    else:
                         places.append({
                    "city": row[0],
                    "attraction": row[1],
                    "attraction1": row[2],
                    "attraction2": row[3] 
                    })
                        
        col_name = request.form.get('check')
      #  print(col_name)

        ngram_size = 1
        nb_spam_model = open("pretrainedModel/NB_model.pkl", 'rb')
        clf = joblib.load(nb_spam_model)

        dictionary_filepath = open("pretrainedModel/vocabulary_model.pkl", 'rb')
        vocabulary_to_load = joblib.load(dictionary_filepath)
        loaded_vectorizer = CountVectorizer(ngram_range=(ngram_size, ngram_size), min_df=1, vocabulary=vocabulary_to_load)
        loaded_vectorizer._validate_vocabulary()

        df1 = pd.read_csv(file_path,skiprows=1,names=['col_1','col_2','col_3'] , encoding='latin-1')
        our_list=df1['col_1']

        sre=[]
        for name in our_list:
            inp1 = [name]
            inp1 = loaded_vectorizer.transform(inp1).toarray()
            my_prediction1 = clf.predict(inp1)
            sre.append(my_prediction1)
         #   print(my_prediction1)
        
        fields = ['Sentiment'] 

        with open("predictCsv/Predict_sentiment.csv", 'w' ,newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(fields)
            writer.writerows(sre)


        df2=pd.read_csv(file_path)
        df3=pd.read_csv("predictCsv/Predict_sentiment.csv")
        df4 = pd.concat([df2, df3], axis=1, join='inner')
        #df4.set_index('sentiment', inplace=True)

        
        df4.to_csv('predictCsv/combine.csv')

    return render_template('csvfilechoose.html',places=places,title='Choose CSV file')