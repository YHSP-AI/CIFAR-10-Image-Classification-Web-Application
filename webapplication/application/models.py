from application import db
from flask_login import UserMixin
import re 
from werkzeug.security import generate_password_hash , check_password_hash

regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
class User(UserMixin , db.Model):
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable = False , unique = True)
    password = db.Column(db.String, nullable = False )
    
    def __init__(self, **data):
        self.username = data['username']
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if not re.fullmatch(regex, self.username):
            raise Exception('Username must be in email format')
        
        if len(data['password']) < 6:
            raise Exception('Password must be 6 characters long')
        
        
        self.username = data['username']
        
        data['password'] = generate_password_hash(data['password'])

        
         
        super().__init__(**data )





class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column( db.String ,  nullable=False , unique = True )
    predicted_on = db.Column(db.DateTime, nullable=False)
    userid = db.Column(db.Integer, db.ForeignKey('user.id') , nullable = False)
    predictedClass  = db.Column(db.Integer, nullable = False)
    
    model  = db.Column(db.String, nullable = False)
    
    
    
    def __init__(self, **data):
        self.model = data['model']
        if data['model'] not in {'wideresnet' ,'vgg'}:
            raise Exception('Model must only be wideresnet or vgg')
        
        if data['predictedClass'] < 0 or data['predictedClass'] > 99 :
            raise Exception('Prediction must only be between 0 and 99 inclusive')
        
        
        

        
         
        super().__init__(**data )
    