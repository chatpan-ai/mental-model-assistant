# -*- encoding: utf8 -*- 

import json

from fastapi import FastAPI

import requests

app = FastAPI()


CP_API_KEY = '4d38f59ed2e7ce04a2ece0bcf630b3237987b137479bfaef471820b67eda55fb'

RA_ROOM_UUID = '5cb3156a-ff10-4345-a6b0-4650b44ce719'
RA_ASS_UUID = 'd2d38f1a-08a6-4d94-82d8-2c4fe4de0aed'

CP_HOST = 'http://o.chatpan.ai'
ASK_URL = f"{CP_HOST}/api/v1/ask"
ASK_HEADERS = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': f"Bearer {CP_API_KEY}"
}


@app.post("/mental_model/process")
async def process_mental_model(request_body: dict):    
    print(request_body)
    q = request_body['dialog']['question']
    


    data = {
        'roomUUID': RA_ROOM_UUID,
        'assistantUUID': RA_ASS_UUID,
        'question': q
    }

    r = requests.post(ASK_URL, headers=ASK_HEADERS, json=data, timeout=180)    
    ra_answer = r.json()['data']['answer']
    
    picked_model_list = json.loads(ra_answer)
    
    print (picked_model_list)
    
    
    model_title_list = []
    model_answer_list = []
    for picked_model in picked_model_list:
        print(f"Get answer from model {picked_model['title']}")
        data = {
            'roomUUID': picked_model['chatpan_room_uuid'],
            'assistantUUID': picked_model['chatpan_assistant_uuid'],
            'question': q
        }
        r = requests.post(ASK_URL, headers=ASK_HEADERS, json=data, timeout=180)    
        ret_json = r.json()
        print(picked_model['title'], ret_json)
        model_answer = ret_json['data']['answer']
        # print(picked_model['title'], model_answer)
    
        model_title_list.append(picked_model['title'])
        model_answer_list.append(model_answer)
    
    
    # get all answers from model, build complete list
    
    content_list = [
        'The Mental Model used ：' + ','.join(model_title_list)
    ]
    
    content_list.extend(model_answer_list)
    

    print(content_list)
    response_body = {
        "code": 200,
        "msg": "OK",
        "data": content_list
    }
    return response_body


@app.get("/mental_model/hello")
async def hello():    
    return 'hello world'


