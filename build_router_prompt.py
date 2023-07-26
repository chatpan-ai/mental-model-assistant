# -*- encoding: utf8 -*- 

import json

import asyncio

import build_model

async def run():
    
    prompt = '''Background: You are an export of Mental Model, you may have a lot of knowledge about Mental Model. 
You can easily find the user's question is about which model. You can also easily find the answer of the question from your knowledge base.
Also, you are a router assistant , there are serial mental model assistant you can invoke. 
You can use your own knowledge or use the mental model assistant to answer the user's question.

Eash mental model assistant has a summary, tags. With the summary and tags, you can easily decide which mental model assistant to invoke.
The mental model's config like this:
{
    "title": "$The title, you can tell user with this title$",
    "summary": "$The summary, you will use the summary to deside if the model works with user's question, if so you will invoke this mental model assistant$",
    "tags": "$An extra information about summary for you to decide if the model works with user's question$",
    "chatpan_assistant_uuid": "$chatpan_assistant_uuid$",
    "chatpan_room_uuid": "$chatpan_room_uuid$"
}

There are model list:
'''
    
    
    model_list_desc = ""
    model_list:list = await build_model.get_all_models()
    for model_info in model_list:
        model_desc = json.dumps(model_info, indent=2, ensure_ascii=False)
        model_list_desc += model_desc + "\n"
        
        
    prompt += model_list_desc
    
    print("background\n\n",prompt)
    
    prompt = '''
Please choose models you want to use, return raw json.
A list of model you choose, each model into a json {}, key is title, chatpan_assistant_uuid and chatpan_assistant_uuid '''

    print('\n\n', '-' * 20, '\n\n')

    print("prompt\n\n",prompt)
    return prompt


if __name__ == "__main__":
    
    asyncio.run(run())
