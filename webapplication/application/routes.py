from application import app
from flask import render_template , request, flash  , redirect , url_for , json, jsonify,send_from_directory
from application.forms import FilterSearchForm , SignUpForm, LoginForm
from application import  manager
from application import db , cifar100classes
from application.models import Prediction , User
from datetime import datetime
from sqlalchemy  import and_, or_, not_  , func
import pandas as pd 
from application import app
from flask import render_template, request, flash
from flask_cors import CORS, cross_origin
from tensorflow.keras.preprocessing import image
# from tensorflow.keras.preprocessing import image
# from tensorflow.keras.utils import img_to_array
import uuid
from PIL import Image, ImageOps , ImageEnhance
import numpy as np
import tensorflow.keras.models
import re
import base64
from io import BytesIO
import json
import numpy as np
import requests
import pathlib, os

from werkzeug.security import generate_password_hash , check_password_hash
from flask_login import login_user , logout_user , login_required , current_user

app.config['predictphotospath'] = os.path.join(app.root_path, 'predphotos')

print(app.config['predictphotospath'])

@manager.user_loader
def loader(userid):
    return User.query.get(int(userid))



@app.route('/predphoto/<path:filename>')
@login_required
def custom_static(filename):
    return send_from_directory(app.config['predictphotospath'], filename)

@app.route('/hello')
def hello_world():
    return "<h1> Hello World </h1>"


@app.route('/')
@app.route('/home')
@app.route('/index')
def home():
    return render_template('index.html' , title = 'Image Classification')

def parseImage(imgData,filepath):
# parse canvas bytes and save as output.png
    print('start parse')
    searched = re.search(b'base64,(.*)', imgData)
    if searched is None:
        imgstr = imgData
    else:
        imgstr = searched.group(1)
    with open(filepath,'wb') as output:
        output.write(base64.decodebytes(imgstr))
    im = Image.open(filepath).convert('RGB')
    im.save(filepath)
    print('end parse')
    
    # im_invert = ImageOps.invert(im)
    # im_invert.save('output.png')



def make_prediction(instances,url):
    data = json.dumps({"signature_name": "serving_default", "instances":instances.tolist()})
    headers = {"content-type": "application/json"}
    json_response = requests.post(url, data=data, headers=headers)
    print(json_response.text)
    print(json.loads(json_response.text))
    predictions = json.loads(json_response.text)['predictions']
    return predictions










@app.route("/apipredict/<model>", methods=['GET','POST'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])#only allow localhost to use this command
@login_required
def predict(model):
# get data from drawing canvas and save as image
    if model == 'wideresnet':
        url = 'https://ca2-tensorflow-serving-model-deployment.onrender.com/v1/models/wideresnet:predict'
    
    else:
        url = 'https://ca2-tensorflow-serving-model-deployment.onrender.com/v1/models/vgg:predict'
        
        

    
    
    uniquecomponent= uuid.uuid4().hex
    photoname= datetime.now().strftime("%m%d%Y,%H%M%S") + uniquecomponent  + '.png'
    
    
    
    filepath =os.path.join(app.config['predictphotospath'], photoname)
    
    # try:
    print('recevied request')
    data = request.get_data()
    # data= request.data
    print('recevied data')
    
    # print(data)
    parseImage(data, filepath)
    unsharped3232 = Image.open(filepath).resize((32,32))
    sharpend3232 = ImageEnhance.Sharpness(unsharped3232).enhance(2)
    # sharpend3232.show() 
    
    img = image.img_to_array(sharpend3232) / 255. 
    # reshape data to have a 3 channel
    img = img.reshape(1,32,32,3)
    predictions = make_prediction(img , url)
    # except Exception as e:
        # print(e)
    # return "Error Predicting" , 400
    
    
    for i, pred in enumerate(predictions):
        ret = "{}".format(cifar100classes[np.argmax(pred)])
        response = ret
    
    
    
    
    predictionrow = Prediction(
        filename = photoname,
        predicted_on = datetime.utcnow(),
        userid = current_user.id, 
        predictedClass = int(np.argmax(pred)) , 
        model = model
    )
    
    
    try:
        db.session.add(predictionrow)
        db.session.commit()
        
    except Exception as e:
        print(e)
        return "Error Predicting" , 400
    
    
    
    
    return response




@app.route("/apipredictproba/<model>", methods=['GET','POST'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])#only allow localhost to use this command
@login_required
def predictproba(model):
# get data from drawing canvas and save as image
    if model == 'wideresnet':
        url = 'https://ca2-tensorflow-serving-model-deployment.onrender.com/v1/models/wideresnet:predict'
    
    else:
        url = 'https://ca2-tensorflow-serving-model-deployment.onrender.com/v1/models/vgg:predict'
        
        

    
    
    uniquecomponent= uuid.uuid4().hex
    photoname= datetime.now().strftime("%m%d%Y,%H%M%S") + uniquecomponent  + '.png'
    
    
    
    filepath =os.path.join(app.config['predictphotospath'], photoname)
    
    # try:
    print('recevied request')
    # data = request.get_data()
    data = request.files.get('image')
    # data= request.data
    print('recevied data')
    
    # print(data)
    # parseImage(data, filepath)
    data.save(filepath)
    unsharped3232 = Image.open(filepath).resize((32,32)).convert('RGB')
    sharpend3232 = ImageEnhance.Sharpness(unsharped3232).enhance(2)
    # sharpend3232.show() 
    
    img = image.img_to_array(sharpend3232) / 255. 
    # reshape data to have a 3 channel
    img = img.reshape(1,32,32,3)
    predictions = np.array(make_prediction(img , url)[0])
    # except Exception as e:
        # print(e)
    # return "Error Predicting" , 400
    
    orderedindices = np.argsort(predictions)[::-1][:5]#top 5 indices
    
    # print(predictions.shape,orderedindices.shape)
    
    # responsedata
    
    top5classes = list(map(cifar100classes.get, orderedindices))
    
    top5probabilities =np.round( predictions[orderedindices],1)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # for i, pred in enumerate(predictions):
    #     ret = "{}".format(cifar100classes[np.argmax(pred)])
    #     response = ret
    
    
    
    
    predictionrow = Prediction(
        filename = photoname,
        predicted_on = datetime.utcnow(),
        userid = current_user.id, 
        predictedClass = int(np.argmax(predictions)) , 
        model = model
    )
    
    
    try:
        db.session.add(predictionrow)
        db.session.commit()
        
    except Exception as e:
        print(e)
        return "Error Predicting" , 400
    
    
    
    
    return {'classes' :list(top5classes), 'probabilities' : list(top5probabilities*100)}
    
    

    
    
@app.route('/predict', methods=['GET','POST'])
@login_required
def predictpage():
    return render_template("prediction.html", title="Image Classification" , index = True )

@app.route('/predhistory', methods=['GET' , 'POST'])#returnn filtered data
@login_required
def predicthist():
    RECORDS_PER_PG =  5
    page  = request.args.get('page', 1, type=int)
    form = FilterSearchForm()
    userid = current_user.id
    print(form.data)
    if request.method == 'POST':
        if form.validate_on_submit():
            print('validated')
            mindate = form.mindate.data
            maxdate = form.maxdate.data
            model = form.model.data
            
            if maxdate is None :
                maxdate =  datetime.utcnow().date()
                
            if mindate is None :
                mindate =  datetime(1900, 1,1).date()#set a very early mindate so that all dates from start of this server would be returned
                
            if model == 'both':
                modelcondition =((Prediction.model == 'wideresnet') | ( Prediction.model == 'vgg'))
                
            else:
                modelcondition = Prediction.model == model
           
                
            
                
            print(mindate, maxdate , model)
            datecondition =(func.date( Prediction.predicted_on )<= maxdate) &  (func.date(Prediction.predicted_on )>= mindate)
            print(datecondition)
            finalcondition  =  ((Prediction.userid == userid)    & modelcondition &datecondition )
            print(finalcondition)
            # breakpoint() 
            #Prediction.query.filter( Prediction.model == form.model.data )
            
            
            predictions = Prediction.query.filter(finalcondition).paginate(page=page, per_page=RECORDS_PER_PG)
        else:
            predictions = Prediction.query.filter_by( userid = userid).paginate(page=page, per_page=RECORDS_PER_PG)
            
    else:
        predictions = Prediction.query.filter_by( userid = userid).paginate(page=page, per_page=RECORDS_PER_PG)
    
    

    return render_template("predictionhistory.html"  , predictions = predictions, title="Image Classification" , index = True  ,
                           class_mapping = cifar100classes, form = form)


# @app.route('/predhistory', methods=['GET' , 'POST'])#returnn filtered data
# @login_required
# def predicthist():
    
    
#     form = FilterSearchForm()
#     userid = current_user.id
#     print(form.data)
#     if request.method == 'POST':
#         if form.validate_on_submit():
#             print('validated')
#             mindate = form.mindate.data
#             maxdate = form.maxdate.data
#             model = form.model.data
            
                
#             print(mindate, maxdate , model)
#             datecondition =and_( Prediction.predicted_on.cast(db.Date) <= maxdate , Prediction.predicted_on.cast(db.Date)  >= mindate)
#             print(datecondition)
            
            
#             predictions = Prediction.query.filter( and_(Prediction.userid == userid  , datecondition, Prediction.model == model)).all()
#         else:
#             predictions = Prediction.query.filter_by( userid = userid).all()
            
#     else:
#         predictions = Prediction.query.filter_by( userid = userid).all()
    
    

#     return render_template("predictionhistory.html"  , predictions = predictions, title="Image Classification" , index = True  ,
#                            class_mapping = cifar100classes, form = form)

@app.route('/remove', methods=['POST'])
def remove():
    req = request.form
    id = req["id"]
    try:
        entry = Prediction.query.get(id) 
        filename = entry.filename
        filepath =os.path.join(app.config['predictphotospath'], filename)
        os.remove( filepath)
        db.session.delete(entry)
        db.session.commit()
    except Exception as error:
        db.session.rollback()
        flash(error,"danger")
    
    
    return redirect('/predhistory')



@app.route('/api/remove/<pid>', methods=['DELETE'])
def deletepredapi(pid):

    try:
        entry = Prediction.query.get(pid) 
        filename = entry.filename
        filepath =os.path.join(app.config['predictphotospath'], filename)
        os.remove( filepath)
        db.session.delete(entry)
        db.session.commit()
    except Exception as error:
        db.session.rollback()
        return {'status' :'Fail'}
    
    
    return {'status' : 'Success'}


@app.route('/logout' , methods = ['GET' , 'POST'])
@login_required
def logout():
    logout_user()
    return redirect('/login')
    
    
    
@app.route('/signup', methods=['GET','POST'] )
def signup():
    form = SignUpForm()
    
    
    if request.method == 'POST':
        if form.validate_on_submit():
            password = form.password.data
            username = form.username.data
            
            
            
            try:
                newuser = User(username  = username, password= password)
                db.session.add(newuser)
                db.session.commit()
                login_user(newuser)#login user after account created successfully
                return redirect('/')
            except:
                flash('Error! Username/email Already exists. Please choose a different one' , 'danger')
                
            

        else:
            flash('Error, Unable to Sign Up' , 'danger')
    return render_template("signup.html", form=form, title="Sign Up" , index = True )

@app.route('/auth/login', methods = ['GET','POST'])
def loginauth():
    data = request.get_json()
    user = User.query.filter_by(username = data['username'] ).first()
    print(user)
    
    if user:
        if check_password_hash(user.password , data['password']):
            login_user(user)
            # return redirect('/'
            return 'Success'
        else:
            return 'Failed wrong password' , 401
    else:
        return 'Failed no such user' , 401


@app.route('/api/adduser', methods = ['GET','POST'])
def adduserapi():
    data = request.get_json()
    newusername , newpassword = data['username'] ,data['password']
    # user = User.query.filter_by(username = data['username'] ).first()
    # print(user)


    try:
        newuser = User(username  = newusername, password= newpassword)
        db.session.add(newuser)
        db.session.commit()
        login_user(newuser)#login user after account created successfully
        
        assert newuser.username ==  newusername 
        assert check_password_hash(newuser.password, newpassword )
        return {'userid':newuser.id}
    except:
        return {'status' :'fail' },400
        

        

@app.route('/login', methods=['GET','POST'] )
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(username = form.username.data ).first()
            if user:
        
                if check_password_hash(user.password , form.password.data):
                    login_user(user)
                    return redirect('/')
            else:
                flash('User does not exist' , 'danger')
                
        else:
            flash('Error, Unable to login' , 'danger')
    return render_template("login.html", form=form, title="Log In" , index = True )




@app.route('/api/getpred/<uid>', methods = ['GET'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])#only allow localhost to use this command
def getpred(uid):
    # data = request.args.get('username')
    id =uid
    
    try:
        
        pred = Prediction.query.filter_by(id = id ).first()
        finaldata = pred.__dict__
        del finaldata['_sa_instance_state']
        print(finaldata)
        
        return {'status' :'successful' , 'data' : finaldata}
    except:
        return {'status' :'unccessful'} , 400
    
    
    
    
    






@app.route('/api/storeprediction', methods = ['POST'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])#only allow localhost to use this command
def storepredictionjson():
    data = request.get_json()
    filename = data['filename']
    predictedclass = data['predictedClass']
    model =data['model']

    newpred = Prediction(
          filename = filename,
        predicted_on = datetime.utcnow(),
        userid = data['userid'], 
        predictedClass = predictedclass, 
        model = model
            
        )
    

    try:
        db.session.add(newpred)
        db.session.commit()
        
        assert newpred.filename == filename 
        assert newpred.predictedClass == predictedclass 
        assert newpred.model == model 

        
        return {'id' : newpred.id }
    except Exception as e:
        print(e)
        db.session.rollback() 
        return {'status' :'fail'}, 400 



    

# @app.route('/api/adduser', methods = ['POST'])
# @cross_origin(origin='localhost',headers=['Content- Type','Authorization'])#only allow localhost to use this command
# def storeuser():
#     data = request.get_json()
#     username = data['username']
#     password = data['password']
    
    
#     try:
        
    
#         newuser = User( username = username , password = password)
        
#         db.session.add(newuser)
#         db.session.commit() 
        
#         assert newuser.username ==  username 
#         assert check_password_hash(newuser.password, password )
#         return {'status' :newuser.id}
#     except Exception as e:
#         print(e)
#         db.session.rollback()
#         return {'status' : 'fail'} , 400
    

