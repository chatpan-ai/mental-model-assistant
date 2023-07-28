# -*- encoding: utf8 -*- 

import json, time

from fastapi import FastAPI

import requests

import build_model

app = FastAPI()


CP_API_KEY = 'YOUR_CHATPAN_API_KEY'

RA_ROOM_UUID = 'dba5df4b-8008-45ec-ae96-48a29f5fb74c'
RA_ASS_UUID = '6ccea77c-2116-4bf1-830a-e739c30bddc2'

CP_HOST = 'https://chatpan.ai'
ASK_URL = f"{CP_HOST}/api/v1/ask"
MULTI_ASK_URL = f"{CP_HOST}/api/v1/multiAsk"
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
    
    print(f"💡 Thinking which model should pick")

    time_s = time.time()
    r = requests.post(ASK_URL, headers=ASK_HEADERS, json=data, timeout=180)    
    time_e = time.time()
    
    # print('ra json', r.json())

    ra_answer = r.json()['data']['answer']
    
    picked_model_list = []
    try:
        picked_model_list = json.loads(ra_answer)
    except:
        print(q, ra_answer)
        response_body = {
            "code": 200,
            "msg": "OK",
            "data": []
        }
        return response_body
    
    
    print(f"{picked_model_list} cost {time_e - time_s} seconds")
    

    model_list:list = await build_model.get_all_models()
    
    model_dict:dict = {model['id']: model for model in model_list}
    

    model_title_list = []
    model_answer_list = []
    ask_data_list = []
    for picked_model in picked_model_list:
        print(f"Get answer from model {picked_model['title']} id:{picked_model['id']}")
        
        model_title_list.append(picked_model['title'])
        
        model_id = picked_model['id']
        if model_id not in model_dict:
            continue
        
        model = model_dict[model_id]
        
        data = {
            'roomUUID': model['chatpan_room_uuid'],
            'assistantUUID': model['chatpan_assistant_uuid'],
            'question': q
        }
        
        ask_data_list.append(data)
    
        
    time_s = time.time()
    r = requests.post(MULTI_ASK_URL, headers=ASK_HEADERS, data=json.dumps(ask_data_list), timeout=600)    
    time_e = time.time()
    print(f"⚙ Get answer from all model cost {time_e - time_s} seconds")
    ret_json = r.json()
    print('ALL -> ', ret_json)
    
    answer_data_list = ret_json['data']
    model_answer_list = [answer_data['answer'] for answer_data in answer_data_list]
    
    # get all answers from model, build complete list
    
    content_list = [
        'The Mental Model used : <<<' + ','.join(model_title_list) + ">>>\n",
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


