# -*- encoding: utf8 -*- 

import asyncio
import ormar

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


async def get_all_models():
    model_list = [
        {
            "title": "第一曲线",
            "summary" : "第一曲线是指创新的元模型中的一种曲线形态。在商业中，创新的目的是为了增长。第一曲线代表着企业在创新初期通过连续性创新实现增长的阶段。然而，随着时间的推移和市场的饱和，企业会遭遇到一个极限点，即第一曲线的终点，此时企业的增长势头会停止或开始下降。极限点是不可避免的，而且随着技术进步的加速，极限点出现的频率也越来越快。",
            "tags" : "",
            "chatpan_assistant_uuid": "481401be-053b-4246-ac1b-0244e1cbe6d2",
            "chatpan_room_uuid": "c1658561-54b8-4485-8bb0-862ffab38dda"
        }, {
            "title": "组合创新",
            "summary" : "组合创新是指将已有的要素重新组合，创造出新的组合形式。它不是从无到有地创造新事物，而是将不同的事物关联起来形成新的事物。组合创新的核心是拆解基本要素，洞察关键要素，并将它们重新组合。这种创新方法可以应用于各个领域，包括科技、商业等。",
            "tags" : "",
            "chatpan_assistant_uuid": "7540b2a8-8059-4ad1-afdc-4408fb017565",
            "chatpan_room_uuid": "21371694-b91a-43b0-8b50-916c597aba26"
        }, {
            "title": "第二曲线",
            "summary" : "第二曲线是指在企业发展过程中，当第一条曲线（即主要业务的增长曲线）达到极限点时，启动并发展起来的新的业务增长曲线。它代表了一种跳跃式、非连续性的创新和发展方式。通过开启第二曲线，企业能够应对市场的变化和挑战，实现持续的增长和创新。",
            "tags" : "",
            "chatpan_assistant_uuid": "54859347-3ebc-4c3d-ba70-2c23c3eec01f",
            "chatpan_room_uuid": "fa641dd0-bb7c-4cb8-9b3a-7d5358dc28d4"
        }
    ]

    '''
    for model_info in model_list:
        build_model(model_info)
    '''
    
    return model_list    
        
if __name__ == '__main__':
    
    asyncio.run(get_all_models())

    