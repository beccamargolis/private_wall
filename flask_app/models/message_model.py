from sqlite3 import connect
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Message:
    db_name = 'private_wall_schema'
    def __init__(self,db_data):
        self.id = db_data['id']
        self.sender_id = db_data['sender_id']
        self.receiver_id = db_data['receiver_id']
        self.receiver = db_data['receiver']
        self.sender = db_data['sender']
        self.content = db_data['content']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']

    
    @classmethod
    def get_user_messages(cls,data):
        query = "SELECT users.first_name AS sender, users2.first_name AS receiver, messages.* FROM users LEFT JOIN messages ON users.id = messages.sender_id LEFT JOIN users AS users2 ON users2.id = messages.receiver_id WHERE users2.id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        messages = []
        for message in results:
            messages.append(cls(message))
        return messages

    @classmethod
    def save(cls,data):
        query = "INSERT INTO messages (sender_id,receiver_id,content) VALUES (%(sender_id)s,%(receiver_id)s,%(content)s);"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def destroy(cls,data):
            query = "DELETE FROM messages WHERE messages.id = %(id)s;"
            return connectToMySQL(cls.db_name).query_db(query,data)