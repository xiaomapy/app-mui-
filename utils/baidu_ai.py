import os
import settings
from uuid import uuid4
from aip import AipSpeech
from aip import AipNlp
from utils.tuling_robot import request_TuLing
client = AipSpeech(settings.APP_ID, settings.API_KEY, settings.SECRET_KEY)
nlp_client = AipNlp(settings.APP_ID, settings.API_KEY, settings.SECRET_KEY)


def get_file_content(filePath):
    '''
    音频格式转换
    :param filePath:
    :return:
    '''
    os.system(
        'ffmpeg -y -i %s  -acodec pcm_s16le -f s16le -ac 1 -ar 16000 %s.pcm' % (filePath, filePath))  # 将语音文件转化成pcm格式
    # os.system()运行shell命令，直接显示
    with open('%s.pcm' % (filePath), 'rb') as fp:
        return fp.read()


# ######  语音转文字  ######
def Voice_to_text(file_name):
    '''
    语音转文字
    :return:
    '''

    speech_file = get_file_content(file_name)

    res = client.asr(speech_file, 'pcm', 16000, {
        'dev_pid': 1536,
    })
    question = res.get('result')[0]
    if res.get('result'):
        print(question)
    else:
        print(res)
    return question


# ######  文字转语音  ######
def Text_to_speech(text):
    '''
    文字转化语音
    :param text:
    :return:
    '''
    result = client.synthesis(text, 'zh', 1, settings.SPEECH)

    file_name = "%s.mp3" %uuid4()

    file_path = os.path.join(settings.CHAT_FILE, file_name)
    with open(file_path, "wb") as f:
        print(file_name)
        f.write(result)

    return file_name



def my_knowledge_base(question, user_id):
    '''
    个人知识库
    :param question:
    :return:
    '''
    Answer = '我不知道你在说什么'
    print(nlp_client.simnet(question, '你叫什么名字'))  # {'error_msg': 'No permission to access data', 'error_code': 6}
    if nlp_client.simnet(question, '你叫什么名字').get("score") >= 0.7:
        Answer = '我叫小明'
        return Answer

    if nlp_client.simnet(question, '你今年几岁了').get("score") >= 0.7:
        Answer = '我今年8岁了'
        return Answer

    Answer = request_TuLing(question, user_id)
    print(Answer)
    return Answer
