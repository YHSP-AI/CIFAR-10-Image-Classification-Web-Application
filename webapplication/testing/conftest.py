import pytest 
from application import app, db , models
from werkzeug.security import generate_password_hash , check_password_hash
from collections import namedtuple
import json
# @pytest.fixture()
# def new_application():
#     print('called')
#     from application import app , db 
#     yield app , db
    
def login(client,username,password):
    return client.post(
        "/auth/login",
        data=json.dumps(dict(username=username, password=password)),
        content_type="application/json",
    )
    
@pytest.fixture()
def application_client( ):
    # application, db .= new_application
    from application import app , db  , models

    with app.app_context():

        username = 'valid1.email@gmail.com' 
        password = ('password')#create a random user so that it is possible to interact with database

        # db.session.add(user)
        # db.session.commit()

        client = app.test_client()
        with client:
            
            createduserresponse = client.post(
            "/api/adduser",
            data=json.dumps(dict(username=username, password=password)),
            content_type="application/json",
            )
            print(createduserresponse)



            status = client.post(
            "/auth/login",
            data=json.dumps(dict(username=username, password=password)),
            content_type="application/json",
            )
            print(status.get_data(as_text=True))



            yield   dict(context = client , userid =json.loads(createduserresponse.get_data(as_text=True))['userid']) 


            db.session.query(models.User).delete()
            db.session.query(models.Prediction ).delete() 
            db.session.commit()





# print(application_client())
    
# @pytest.fixture()
# def application_client_retrieve( ):
#     # application, db .= new_application
#     from application import app , db  , models

#     with app.app_context():
#         user = models.User(username = 'valid1.email@gmail.com' , password = ('password'))#create a random user so that it is possible to interact with database

#         db.session.add(user)
#         db.session.commit()
        
#         newpredictionrow = 
        
            
#         yield   dict(context = app.test_client() , userid = user.id ) 
        
        
#         db.session.query(models.User).delete()
#         db.session.query(models.Prediction ).delete() 
#         db.session.commit()
