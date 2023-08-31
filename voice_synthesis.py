import requests
import json
import base64
import sys
from multiprocessing import  Process


header = {"Content-Type": "application/json"}
post_dict = {'text': '', 'lang_type': 'my-MM', 'format': 'wav'}


def synthesis_post(list_index, index, text, lang):
    post_dict['text'] = text
    post_dict['lang_type'] = lang
    post_json = json.dumps(post_dict)
    response = requests.post("http://127.0.0.1:7200/stream/v1", data=post_json, headers=header)
    if response.status_code != 200:
        status = "1-00200\n"
        wav_data = ""
    result_dict = dict(response.json())
    if result_dict['status'] != '00000':
        status = "1-%s\n"%(result_dict['status'])
        wav_data = ""
    else:
        status = "0-00000"
        wav_data = base64.b64decode(result_dict['data'])
        f1=open('%s-%s-%s.wav'%(status, list_index, index), 'wb')
        f1.write(wav_data)



def voice_synthesis(list_index, text_list, text_lang):
    maxlen = len(text_list)
    for i in range(0,maxlen):
        synthesis_post(list_index, i, text_list[i], text_lang)


def split_list(in_list, split_num):
    one_size = int(len(in_list)/split_num)
    split_list = [in_list[i:i+one_size] for i in range(0, len(in_list), one_size)]
    if len(split_list) > split_num:
        split_list[-2] = split_list[-2] + split_list[-1]
    return split_list[0:split_num]

if __name__ == '__main__':
    process_list_path = sys.argv[1]
    out_dir_path = sys.argv[2]
    multi_process_num = int(sys.argv[3])
    process_lang = sys.argv[4]
    f1 = open(process_list_path, 'rb', encoding='utf-8')
    f1_lines = f1.readlines()
    process_lines_list = split_list(f1_lines, multi_process_num)
    process_list = []
    for i in range(multi_process_num):  #开启5个子进程执行fun1函数
        p = Process(target=voice_synthesis, args=(i, process_lines_list[i], process_lang, )) #实例化进程对象
        p.start()
        process_list.append(p)

    for p in process_list:
        p.join()
