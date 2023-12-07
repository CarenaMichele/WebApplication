from flask import Flask, render_template, request, redirect, url_for
from datetime import date

app= Flask(__name__) #qualunque sia il nome dell'app viene rimpiazzato in tempo di esecuzione

posts=[
       {'id':0, 'username': 'Davide', 'data': '2 giorni fa', 'testo': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore' 
         'magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit'
         'in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', 
        'imgProfilo': 'img/facciaD.jpg', 'imgPost': 'img/davide.jpg', 'comment_list':[]},
       {'id':1, 'username': 'Michele', 'data': '2 giorni fa', 'testo': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore' 
         'magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit'
         'in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', 
        'imgProfilo': 'img/facciaM.jpg', 'imgPost': 'img/davide.jpg', 'comment_list':[]},
       {'id':2, 'username': 'Federico', 'data': '2 giorni fa', 'testo': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore' 
         'magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit'
         'in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', 
        'imgProfilo': 'img/facciaF.jpg', 'imgPost': 'img/davide.jpg', 'comment_list':[]}
]



@app.route('/')  #quando il server riceve una richiesta get in questo caso, allora deve eseguire il contenuto della funzione
def index():
   return render_template('index.html', post=posts)

@app.route('/chi_siamo')
def chi_siamo():
   return render_template('chi_siamo.html')

@app.route('/post/<int:id>')
def post(id):
   singlePost=posts[id]
   #comm=[]
   #for i in enumerate(comments):
   #   if id == comments[i]['postRelativo']:
   #      comm.appends(comments[i])
   #app.logger.info(comm)
   return render_template('post.html', singlePost=singlePost)

@app.route('/newPost', methods=['POST'])
def new_post():
   post=request.form.to_dict()
   if post['username']=='':
      app.logger.error('Il campo nome non può essere vuoto')
      return redirect(url_for("index"))
   if post['testo']=='':
      app.logger.error('Il campo testo non può essere vuoto')
      return redirect(url_for("index"))
   if post['data']=='':
      app.logger.error('Il campo data non può essere vuoto')
      return redirect(url_for("index"))
   current_date= date.today()
   str_date= current_date.strftime("%Y-%m-%d")
   app.logger.info(str_date)
   app.logger.info(post['data'])
   if post['data']<str_date:
      app.logger.error('Il campo data deve essere uguale o successivo alla data corrente')
      return redirect(url_for("index"))
   
   foto = request.files['imgPost']
   if foto:
      foto.save('static/img/'+ foto.filename)
      post['imgPost'] = 'img/'+foto.filename

   post['id'] =posts[-1]['id']+ 1
   post['imgProfilo'] =posts[0]['imgProfilo']
   posts.append(post)
   app.logger.info(posts)
   #app.logger.debug(request.form['username'])
   return redirect(url_for("index"))

@app.route('/newComment/<int:id>', methods=['POST'])
def new_comment(id):
   app.logger.info(id)
   commento=request.form.to_dict()
   app.logger.info(commento)
   if commento['username']=='':
      commento['username']='Anonimo'
      app.logger.info('Il nome è anonimo')
   else:
      app.logger.info('il nome è ' + commento['username'])
   if commento['commento']=='':
      app.logger.error('Il campo commento non può essere vuoto')
   if 'rating' in commento:
      app.logger.info('il rating ' + commento['rating'])
   else:
      commento['rating']= 1
   foto = request.files['imgCommento']
   if foto:
      foto.save('static/img/imgCommenti/'+ foto.filename)
      commento['imgCommento'] = 'img/imgCommenti/'+foto.filename
   else:
      commento['imgCommento'] ='img/icon.jpg'
   
   posts[id]['comment_list'].append(commento)

   app.logger.info(posts)

   return redirect(url_for("post", id=id))