from flask import Flask,request,render_template,redirect,url_for,json
from flask import jsonify
import numpy as np
import pandas as pd
from fuzzywuzzy import fuzz
from tmdbv3api import TMDb
import json
import requests
tmdb = TMDb()
tmdb.api_key = '14762c35fc347b042a13807d3524e74f'
from tmdbv3api import Movie
tmdb_movie = Movie()
app=Flask(__name__)

@app.route('/')
def hello_world():
    x=''
    return render_template("index.html",recc=json.dumps(x))

@app.route('/reccomend',methods=['POST','GET'])
def reccomend():
    recc=[]
    df1=pd.read_csv('last.csv')
    name=request.form.get('name')
    name=name.lower()
    try:
        if request.method == "POST":
            """sim=pd.read_csv('similarity.csv')
            df.set_index(df['movie_title'],inplace=True)
            index=pd.Series(df.index)
            idx=index[index==name].index[0]
            row=pd.Series(sim.iloc[:,idx])
            row=row.sort_values(ascending=False)
            row=row[1:11].index   
            for i in row:
                recc.append(list(df.index)[i])

            #res="Reccomended movies related to your search: <br>"
            #for i in range(len(recc)):
            #    res=res + recc[i]+ ' '
            #recc=res"""
            df1.set_index(df1['movie_title'],inplace=True)
            df2=pd.read_csv('similarity.csv')
            index=pd.Series(df1.index)
            idx=index[index==name].index[0]
            row=pd.Series(df2.iloc[:,idx])
            row=row.sort_values(ascending=False)
            row=row[1:13].index
            ans={}
            for i in row:
                movie_name=df1.index[i]
                result=tmdb_movie.search(movie_name)
                path=''
                if not result:
                    path=''
                else:
                    movie_id=result[0].id
                    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key={}'.format(movie_id,tmdb.api_key))
                    data=response.json()
                    if data['poster_path']:
                        poster='https://image.tmdb.org/t/p/w185'
                        poster=poster+data['poster_path']
                        path=poster
                    else:
                        path=''
                ans.update({movie_name.title():path})
            recc=ans
    except:
        match=[]
        df1=pd.read_csv('last.csv')
        for m in df1['movie_title']:
            ratio=fuzz.ratio(m.lower(),name.lower())
            if ratio >= 60:
                match.append(m)
        match=sorted(match,reverse=True)
        #match=match[:5]
        df1.set_index(df1['movie_title'],inplace=True)
        if not match:
            recc='No match found'
        else:
            #recc=match
            #recc="No movie , try searching for "
            #for i in match:
             #   recc=recc + i + " , " 
            ans={}
            for i in match:
                movie_name=i
                result=tmdb_movie.search(movie_name)
                path=''
                if not result:
                    path=''
                else:
                    movie_id=result[0].id
                    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key={}'.format(movie_id,tmdb.api_key))
                    data=response.json()
                    if data['poster_path']:
                        poster='https://image.tmdb.org/t/p/w185'
                        poster=poster+data['poster_path']
                        path=poster
                    else:
                        path=''
                ans.update({movie_name.title():path})
            recc=ans
    return render_template('index.html',recc=json.dumps(recc))

@app.route('/details/<string:info>',methods=['POST'])
def details(info):
    movie_name =json.loads(info).lower()
    df1=pd.read_csv('last.csv')
    ans={}
    ans.update({'Movie':movie_name.title()})
    t=df1['director_name'].loc[df1['movie_title']==movie_name].values[0]
    #t=str(t)
    ans.update({'Director':t.title()})
    t=df1['actor_3_name'].loc[df1['movie_title']==movie_name].values[0]
    #t=str(t)
    ans.update({'Third Actor':t.title()})
    t=df1['actor_2_name'].loc[df1['movie_title']==movie_name].values[0]
    #t=str(t)
    ans.update({'Second Actor':t.title()})
    t=df1['actor_1_name'].loc[df1['movie_title']==movie_name].values[0]
    #t=str(t)
    ans.update({'First Actor':t.title()})
    t=df1['genres'].loc[df1['movie_title']==movie_name].values[0]
    #t=str(t)
    ans.update({'Genres':t.title()})
    #ans=str(ans)
    #calculating poster path
    result=tmdb_movie.search(movie_name)
    path=''
    if not result:
        path=''
    else:
        movie_id=result[0].id
        response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key={}'.format(movie_id,tmdb.api_key))
        data=response.json()
        if data['poster_path']:
            poster='https://image.tmdb.org/t/p/w185'
            poster=poster+data['poster_path']
            path=poster
        else:
            path=''
    ans.update({'poster':path})
    return ans
if __name__=='__main__':
    app.run(debug=True)