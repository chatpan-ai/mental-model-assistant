# -*- encoding: utf8 -*- 

import json

import asyncio

import build_model

async def run():
    
    prompt = '''You are an export of Mental Model, you may have a lot of knowledge about Mental Model. 
You are a router assistant , there are serial mental model assistant you can invoke. 

Use your own knowledge base and the summary in mental model assistants to decide which mental model assistant fit the situation in user's question.

The mental model's config like this:
{
    "title": "$The title, you can tell user with this title$",
    "summary": "$The summary, you will use the summary to deside if the model works with user's question, if so you will use this mental model assistant$",
    "tags": "$An extra information about summary for you to decide if the model works with user's question$",
    "id": "$model unique id$"
}

There are model list:
'''
    
    
    model_list_desc = ""
    model_list:list = await build_model.get_all_models()
    for model_info in model_list:
        model_prompt_json = {
            "title": model_info['title'],
            "summary": model_info['summary'],
            # "tags": model_info['tags'],
            "id": model_info['id']
        }
        model_desc = json.dumps(model_prompt_json, indent=2, ensure_ascii=False)
        model_list_desc += model_desc + "\n"
        
        
    prompt += model_list_desc
    
    print("background\n\n",prompt)
    
    prompt = '''At most you can choose 6 most suitable models in assistants list.
Please choose models you want to use, return raw json.
A list of model you choose, each model into a json {[]}, key is title, id. If nothing picked, return empty list.'''

    print('\n\n', '-' * 20, '\n\n')

    print("prompt\n\n",prompt)
    return prompt


if __name__ == "__main__":
    
    asyncio.run(run())
