from app.Models.User import User
from flask import jsonify, request, render_template, redirect, url_for

class UserController:
    def index():
        return render_template('users/index.html',users =User.query.all())

    def create():
        return render_template('users/create.html')

    def store():
        User().create(request.form)
        return redirect(url_for('users.index'))

    def show(id):
        return render_template('users/show.html',user =User.query.get(id))

    def edit(id):
        return render_template('users/edit.html',user =User.query.get(id))

    def update(id):
        User.query.get(id).update(request.form)
        return redirect(url_for('users.index'))
    
    def delete(id):
        User.query.get(id).delete()
        return redirect(url_for('users.index'))
