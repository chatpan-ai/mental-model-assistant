# -*- encoding: utf8 -*- 

import json

import asyncio
import ormar

import pandas as pd


from db import MentalModel


async def build_model(model_info:dict):
    
    try:
        model = await MentalModel.objects.get(title=model_info['title'])
    except ormar.exceptions.NoMatch:
        model = MentalModel(
            title = model_info['title']
        )
        await model.save()
    
    model.summary = model_info['summary']
    model.tags = model_info['tags']
    model.chatpan_assistant_uuid = model_info['chatpan_assistant_uuid']
    
    await model.save()

async def get_all_models(model_json_file:str = 'models/models.json'):
    
    return json.loads(open(model_json_file, 'r').read())
    
async def write_all_models(file_path:str, to_file:str):
    
    df = pd.read_excel(file_path, sheet_name="models")
    
    model_data_list = []
    id_idx = 0
    for index, row in df.iterrows():
        id_idx = id_idx + 1
        
        model_data_list.append({
            "id": id_idx,
            "title": row['title'].strip(),
            "summary" : row['summary'].strip(),
            # "tags" : row['tags'],
            "chatpan_assistant_uuid": row['chatpan_assistant_uuid'].strip(),
            "chatpan_room_uuid": row['chatpan_room_uuid'].strip()
        })
    
    

    # for model_info in model_data_list:
    #     # build_model(model_info)
    #     print(model_info)
        
    open(to_file, 'w').write(json.dumps(model_data_list, indent=2))
    
    return model_data_list    
        
if __name__ == '__main__':
    
    asyncio.run(write_all_models('models/models.xlsx', 'models/models.json'))

    