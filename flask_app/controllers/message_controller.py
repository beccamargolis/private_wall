from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user_model import User
from flask_app.models.message_model import Message
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/post/message',methods=['POST'])
def post_message():
    if 'user_id' not in session:
        return redirect('/')

    data = {
        "sender_id": request.form['sender_id'],
        "receiver_id": request.form['receiver_id'],
        "content": request.form['content']
    }
    Message.save(data)
    return redirect('/dashboard')

@app.route('/destroy/message/<int:id>')
def destroy(id):
    data = {
        "id": id
    }
    Message.destroy(data)
    return redirect('/dashboard')