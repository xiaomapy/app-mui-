import requests
import json

TuLing_url = 'http://openapi.tuling123.com/openapi/api/v2'
data = {
    "reqType": 0,
    "perception": {
        "inputText": {
            "text": '北京今天，天气怎么样'
        }
    },
    "userInfo": {
        "apiKey": "8f2ca9a744054a5f8be28131ee860db7",
        "userId": "tutu"
    }
}


def request_TuLing(question, user_id):
    '''

    :param data:
    :return:
    '''
    data['perception']['inputText']['text'] = question
    data['userInfo']['userId'] = user_id
    res = requests.post(TuLing_url, json=data)
    res_dict = json.loads(res.content.decode('utf8'))  # type:dict
    res_type = res_dict.get('results')[0].get('resultType')
    result = res_dict.get('results')[0].get('values').get(res_type)

    return result
