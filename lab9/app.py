from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import date
import posts_dao, os

app= Flask(__name__) #qualunque sia il nome dell'app viene rimpiazzato in tempo di esecuzione
app.config['SECRET_KEY']=os.urandom(24)

@app.route('/')  #quando il server riceve una richiesta get in questo caso, allora deve eseguire il contenuto della funzione
def index():
   posts = posts_dao.get_posts()
   return render_template('index.html', post=posts)

@app.route('/chi_siamo')
def chi_siamo():
   return render_template('chi_siamo.html')

@app.route('/post/<int:id>')
def post(id):
   singlePost=posts_dao.get_post(id)
   comments= posts_dao.get_comments(id)
   return render_template('post.html', singlePost=singlePost, comments= comments)

@app.route('/newPost', methods=['POST'])
def new_post():
   try:
      post=request.form.to_dict()
      if post['username']=='':
         raise Exception
      if post['testo']=='' or len(post['testo']<30):
         raise Exception
      if post['data']=='':
         raise Exception
      current_date= date.today()
      str_date= current_date.strftime("%Y-%m-%d")
      app.logger.info(str_date)
      app.logger.info(post['data'])
      if post['data']<str_date:
         raise Exception
      
      foto = request.files['imgPost']
      if foto:
         foto.save('static/img/'+ foto.filename)
         post['imgPost'] = 'img/'+foto.filename
      else:
         post['imgPost'] = ' '
   
   #post['imgProfilo'] =posts[0]['imgProfilo']
      post['imgProfilo']='img/icon.jpg'
      success = posts_dao.add_post(post)

      if success:
         flash('Post creato correttamente', 'success')
      else:
         raise Exception
         
   except Exception:
      flash('Errore nella creazione del post: riprova!', 'danger')

   # post['id'] =posts[-1]['id']+ 1
   # posts.append(post)
   # app.logger.info(posts)
  
   return redirect(url_for("index"))

@app.route('/newComment/<int:id>', methods=['POST'])
def new_comment(id):
   try:
      commento=request.form.to_dict()
      app.logger.info(commento)
      if commento['username']=='':
         commento['username']='Anonimo'
      if commento['commento']=='':
         raise Exception
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
      commento['post_id']=id
      success= posts_dao.add_comment(commento)

      if success:
         flash('Commento creato correttamente!', 'success')
      else:
         raise Exception
         
   except Exception:
      flash('Errore nella creazione del commento: riprova!', 'danger')

   #app.logger.info(posts)

   return redirect(url_for("post", id=id))