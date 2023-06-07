import datetime 
import pytest

import json
import os 
import base64

@pytest.mark.parametrize(
    "data",
    [
        (
            dict(
               filename = 'photo2.jpg',
                predictedClass = 9, 
                model = 'wideresnet'
            )
        ),
        (
            dict(
                filename = 'photo1.jpg',
                predictedClass = 6, 
                model = 'wideresnet'
            )
        ),
         (
            dict(
                filename = 'photo1.jpg',
                predictedClass = 6, 
                model = 'vgg'
            )
        ),
    ],
)
def test_insert_prediction(application_client, data):
    context = application_client["context"]
    userid = application_client["userid"]
    newdata = data.copy()

    newdata["userid"] = userid

    response = context.post(
        "/api/storeprediction",
        data=json.dumps(newdata),
        content_type="application/json",
    )

    assert response.status_code == 200
    assert isinstance(json.loads(response.get_data(as_text=True))["id"], int)


@pytest.mark.xfail(strict=True)  
@pytest.mark.parametrize(
    "data",
    [
        (
            dict(
                filename = 'photo1.jpg',
                predictedClass = 6, 
                model = 'invalidmodel'#invalid model
            )
        ),       
        (
            dict(
                filename = 'photo1.jpg',
                predictedClass = -10, #invalid prediction , value is too low
                model = 'wideresnet'
            )
        ),
        (
            dict(
                filename = 'photo1.jpg',
                predictedClass = 101, #invalid prediction, value is too high
                model = 'wideresnet'
            )
        )
    ],
)
def test_insert_prediction_fail(application_client, data):
    test_insert_prediction(application_client, data)


@pytest.mark.parametrize(  # expected pass user
    "data",
    [
        (
            dict(
                username="valid.email@gmail.com", password="vvvvvvvvalidpasswordlength8"
            )
        ),
        (
            dict(
                username="another.valid.email@gmail.com",
                password="anothervalidpasswordlength8",
            )
        ),
        (dict(username="yhang.21@ichat.sp.edu.sg", password="paswordlength8")),
    ],
)
def test_insert_user(application_client, data):
    context = application_client["context"]
    userid = application_client["userid"]
    response = context.post(
        "/api/adduser", data=json.dumps(data), content_type="application/json"
    )
    assert response.status_code == 200
    assert isinstance(json.loads(response.get_data(as_text=True))["userid"], int)


@pytest.mark.xfail(strict=True)  # Expected Fail email
@pytest.mark.parametrize(
    "data",
    [(dict(username="invalidemail", password="aas")), #both email and password invalid
     (dict(username="", password="")) , # both email and password empty
     (dict(username="valid@gmail.com", password="smal")) , # valid email but invalid password
     (dict(username="lfkdjal;fjdlas;jl", password="validlongpassoword"))],# invalid email but valid password
)
def test_insert_user_fail(application_client, data):
    test_insert_user(application_client, data)



#valid insert prediction into database

@pytest.mark.parametrize(
    "data",
    [
        (
            dict(
                filename = 'photo1.jpg',
                predictedClass = 9, 
                model = 'wideresnet'
            )
        ),
        (
            dict(
                filename = 'photo2.jpg',
                predictedClass = 5 , 
                model = 'vgg'
            )
        ),
    ],
)
def test_get_prediction(application_client, data, create_pred=True):
    context = application_client["context"]
    userid = application_client["userid"]
    newdata = data.copy()

    newdata["userid"] = userid
    if create_pred == True:
        response = context.post(
            "/api/storeprediction",
            data=json.dumps(newdata),
            content_type="application/json",
        )

        newid = json.loads(response.get_data(as_text=True))["id"]
    else:
        newid = 0
    response = context.get(f"/api/getpred/{newid}")
    assert response.status_code == 200
    responsedata = json.loads(response.get_data(as_text=True))
    assert responsedata["data"]
    responsedata = responsedata["data"]
    print(responsedata)
    assert responsedata["filename"] == data["filename"]
    assert responsedata["predictedClass"] == data["predictedClass"]
    assert responsedata["model"] == data["model"]


@pytest.mark.xfail(strict=True)
def test_fail_get_prediction(application_client):
    test_get_prediction(application_client, data=None, create_pred=False)


# ---------------------------------------- Note : This test case takes some time to run, as it needs to post the image to external api (tensorflow serving server) ------------------------------------------------

@pytest.mark.parametrize(
    "data",
    [
        (
            dict(
                filename = 'photo1.jpg',
                predictedClass = 9, 
                model = 'wideresnet'
            )
        ),
        (
            dict(
                filename = 'photo2.jpg',
                predictedClass = 5 , 
                model = 'vgg'
            )
        ),
    ],
)
def test_delete_prediction(application_client, data, create_pred=True):
    context = application_client["context"]
    userid = application_client["userid"]
    newdata = data.copy()

    newdata["userid"] = userid
    if create_pred == True:
        response = context.post(
            "/api/storeprediction",
            data=json.dumps(newdata),
            content_type="application/json",
        )

        newid = json.loads(response.get_data(as_text=True))["id"]
    else:
        newid = 0
    response = context.delete(f"/api/remove/{newid}")
    assert response.status_code == 200



@pytest.mark.xfail(strict=True)
def test_fail_delete(application_client):
    test_delete_prediction(application_client, data=None, create_pred=False)




def read_img_base64(path):
    with open(path, "rb") as img_file:
        my_string = base64.b64encode(img_file.read())
        
    return my_string




@pytest.mark.parametrize(
    "data",
    [
        (
            dict(
                filepath = 'test_img_1.jpg', 
                model = 'wideresnet'
            )
        ),
       (
        dict(
                filepath = 'test_img_1.jpg', 
                model = 'vgg'
            )
       ), 
        (
        dict(
                filepath = 'test_img_2.jpg', 
                model = 'wideresnet'
            )
       ),
        (
        dict(
                filepath = 'test_img_2.jpg', 
                model = 'vgg'
            )
       ),
                (
        dict(
                filepath = 'test_img_3.jpg', 
                model = 'wideresnet'
            )
       ),
        (
        dict(
                filepath = 'test_img_3.jpg', 
                model = 'vgg'
            )
       ),(
          dict(
                filepath = 'lion.webp', 
                model = 'wideresnet'
            )
       ),
        (
        dict(
                filepath = 'lion.webp', 
                model = 'vgg'
            )
       ),(
          dict(
                filepath = 'tv.jpg', 
                model = 'wideresnet'
            )
       ),
        (
        dict(
                filepath = 'tv.jpg', 
                model = 'vgg'
            )
       ),(
          dict(
                filepath = 'fox.png', 
                model = 'wideresnet'
            )
       ),
        (
        dict(
                filepath = 'fox.png', 
                model = 'vgg'
            )
       )
    ],
)
def test_model_consistency(application_client, data):
    # test if model return same prediction everytime same input given
    basepath = os.path.dirname(os.path.abspath(__file__))
    
    filename = data['filepath']
    model  = data['model']
    
    fullpath = os.path.join(basepath, 'test_images', filename)
    
    base64data  = read_img_base64(fullpath)
    
    
    context = application_client["context"]
    userid = application_client["userid"]
    
    
    
    response = context.post(
        f"/apipredict/{model}", data= base64data
    )
    initial_pred = response.get_data(as_text=True)
    print(initial_pred)
    for _ in range(10):
        response = context.post(
            f"/apipredict/{model}", data=base64data
        )

        newpred = response.get_data(as_text=True)

        assert newpred == initial_pred
