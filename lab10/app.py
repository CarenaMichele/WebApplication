from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import date
import posts_dao, os
from flask_login import LoginManager, login_user, login_required, logout_user
from models import User
from werkzeug.security import generate_password_hash, check_password_hash

app= Flask(__name__) #qualunque sia il nome dell'app viene rimpiazzato in tempo di esecuzione
app.config['SECRET_KEY']=os.urandom(24)

login_manager=LoginManager()
login_manager.init_app(app)

@app.route('/')  #quando il server riceve una richiesta get in questo caso, allora deve eseguire il contenuto della funzione
def index():
   posts = posts_dao.get_posts()
   utenti= posts_dao.get_utenti()
   return render_template('index.html', post=posts, utenti=utenti)

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
      #app.logger.info(post['username'])
      if post['username']=='':
         raise Exception
      if post['testo']=='':
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
      #post['imgProfilo']='img/icon.jpg'
      app.logger.info(post)
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
      current_date= date.today()
      str_date= current_date.strftime("%Y-%m-%d")
      commento['dataP']=str_date
      success= posts_dao.add_comment(commento)

      if success:
         flash('Commento creato correttamente!', 'success')
      else:
         raise Exception
         
   except Exception:
      flash('Errore nella creazione del commento: riprova!', 'danger')

   #app.logger.info(posts)

   return redirect(url_for("post", id=id))

"""
@app.route('/iscriviti')
def iscriviti():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup():

  new_user_from_form = request.form.to_dict()

  print(new_user_from_form)

  if new_user_from_form ['nome'] == '':
    app.logger.error('Il campo non può essere vuoto')
    return redirect(url_for('index'))

  if new_user_from_form ['cognome'] == '':
    app.logger.error('Il campo non può essere vuoto')
    return redirect(url_for('index'))

  if new_user_from_form ['email'] == '':
    app.logger.error('Il campo non può essere vuoto')
    return redirect(url_for('index'))

  if new_user_from_form ['password'] == '':
    app.logger.error('Il campo non può essere vuoto')
    return redirect(url_for('index'))
  
  new_user_from_form ['password'] = generate_password_hash(new_user_from_form ['password'])

  success = utenti_dao.creare_utente(new_user_from_form)

  if success:
    return redirect(url_for('index'))

  return redirect(url_for('iscriviti'))

@app.route('/login', methods=['POST'])
def login():

  utente_form = request.form.to_dict()

  utente_db = utenti_dao.get_user_by_email(utente_form['email'])

  if not utente_db or not check_password_hash(utente_db['password'], utente_form['password']):
    flash("Non esiste l'utente")
    return redirect(url_for('index'))
  else:
    new = User(id=utente_db['id'], nome=utente_db['nome'], cognome=utente_db['cognome'], email=utente_db['email'], password=utente_db['password'] )
    login_user(new, True)
    flash('Success!')

    return redirect(url_for('index'))
"""

@login_manager.user_loader
def load_user(user_id):
    db_user=posts_dao.get_user(user_id)
    user = User(id=db_user['utente_id'],	
                username=db_user['username'],		
                password=db_user['password'])
    return user

"""
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
"""