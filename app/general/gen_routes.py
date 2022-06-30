from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)

from app import db

bp_gen = Blueprint('general', __name__, template_folder='templates')
print('name - general', __name__)

bp_blog = Blueprint('blog', __name__,url_prefix='/blog',template_folder="templates")




@bp_blog.route('/blog')
def blog():
    return render_template(
        '/blog/index.html',
        title='blog',
    )

@bp_gen.route('/')
@bp_gen.route('/index')
def index():
    return render_template(
        '/general/index.html',
        title='Home Page',
    )


@bp_gen.route('/getdata')
def get_data():
    text = request.args.get('txt', 0, type=str)

    if text.lower() == 'python':
        return jsonify(result='Выбран правильный язык')
    else:
        return jsonify(result='Попробуйте еще')


@bp_gen.route('/session')
def session():
    return render_template(
        '/general/session.html',
        title='Сессия',
    )


@bp_gen.route('/getsession')
def get_session():
    if request.method == 'GET':
        data = {
            'fam': request.args.get('fam'),
            'age': request.args.get('age'),
            'session': [{'математика': 5},
                        {'Экономика': 4},
                        {'Информатика': 5}]
        }

        print(data)

        return jsonify(data)


@bp_gen.route('/carusel')
def owl():
    return render_template(
        '/general/owl.html',
        title='Карусель',
    )
