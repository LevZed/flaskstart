from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for,jsonify
)
from werkzeug.exceptions import abort

from app.auth.auth_routes import login_required
from app.db import get_db

import json

bp_blog = Blueprint('blog', __name__,url_prefix='/blog',template_folder="templates")


@bp_blog.route('/blog')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()

    return render_template('blog/index.html', posts=posts)


@bp_blog.route('/check', methods=('GET', 'POST'))
@login_required
def check():
   db = get_db()
   if request.method == 'POST':
       
       print(list(request.form.items())) #здесь  видны только отмеченные check's, а также эл-ты с 0-индесом
       
       print('getlist',request.form.getlist('check'))
       
       for key in request.form.keys():
            if key == 'check':
               for value in request.form.getlist(key):
                 print("KEYS", key,":",value)    
                 db.execute('DELETE FROM post WHERE id = ?', (value))
       
       db.commit()

       return redirect(request.origin + url_for('blog.index'))

   posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username, false as del'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()

    
   return render_template('blog/check.html', posts=posts)



@bp_blog.route('/jscheck', methods=('GET', 'POST'))
@login_required
def jscheck():
  
   if request.method=='POST':
        db = get_db()
        keys=request.form.keys() #получим все ключи
        
        lst_keys= list(keys) #преобразуем их в список
        key = lst_keys[0] #возьмем 1-й и единственный ключ - arr
        #этот ключ представляет строковое выражение исходного массива объектов
        jsn  = json.loads(key) # построим JSON-объект из строки
        print('JSON ', jsn)

        for x in jsn['arr']: # arr - это единственный ключ; его значение - список объектов
            print('curr obj: ',x)
            x['name'] = x['name'].upper()
            x['age'] += 5
    


        return jsonify(result = jsn['arr'])
   return "hi"
   



@bp_blog.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            # return redirect(url_for('blog.index'))
            return redirect(request.origin + url_for('blog.index'))

    return render_template('blog/create.html')  


def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post



@bp_blog.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            # return redirect(url_for('blog.index'))
            return redirect(request.origin + url_for('blog.index'))

    return render_template('blog/update.html', post=post) 

@bp_blog.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    # return redirect(url_for('blog.index'))  
    return redirect(request.origin + url_for('blog.index'))       