import pytest
import requests
import base64
import json
from tensorflow.keras.datasets.cifar100 import load_data
import numpy as np
#load MNIST dataset
(_, _), (x_test, y_test) = load_data()

x_test = x_test.astype('float32') / 255.0

def make_prediction(instances , url):
    data = json.dumps({"signature_name": "serving_default",
    "instances": instances.tolist()}) #see [C]
    headers = {"content-type": "application/json"}
    json_response = requests.post(url, data=data, headers=headers)
    return json_response

def test_prediction():
    vggurl =  'https://ca2-tensorflow-serving-model-deployment.onrender.com/v1/models/vgg:predict'
    wideresneturl =  'https://ca2-tensorflow-serving-model-deployment.onrender.com/v1/models/wideresnet:predict'
    
    json_response = make_prediction(x_test[0:4] , vggurl) 
    assert json_response.ok
    assert json.loads(json_response.text)['predictions'] is not None
    predictions = json.loads(json_response.text)['predictions']
    assert isinstance(predictions , list ) 
    print(predictions)
    
    
    json_response = make_prediction(x_test[0:4] , wideresneturl) 
    assert json_response.ok
    assert json.loads(json_response.text)['predictions'] is not None
    predictions = json.loads(json_response.text)['predictions']
    assert isinstance(predictions , list ) 
    print(predictions)
