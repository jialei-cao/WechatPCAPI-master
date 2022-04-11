# -*- coding: utf-8 -*-
# @Time    : 2022/03/28 11:23
# @Author  : 爱摇尾巴的小狗狗
# @File    : receiveMsg.py
# @Desc    :
import sys

from WechatPCAPI import WechatPCAPI
import time
import logging
from queue import Queue
import threading

formatter = logging.Formatter('%(asctime)s-%(levelname)s-%(message)s')
logger = logging.getLogger('receive')
logger.setLevel(logging.INFO)
fh = logging.FileHandler('receive.log')
fh.setFormatter(formatter)
sh = logging.StreamHandler(sys.stdout)
sh.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(sh)
queue_recved_message = Queue()


# 这是消息回调函数，所有的返回消息都在这里接收，建议异步处理，防止阻塞
def on_message(message):
    logger.info("message:"+str(message))
    # 过滤收到的消息,消息类型是群消息,群名称是'终端测试部',send_or_recv:0代表是收到的消息,data_type:1代表仅接收文字,并且信息是'获取key'
    if message.get('type') == 'msg::chatroom' and message.get('data').get('from_chatroom_nickname') == '群聊测试' \
            and message.get('data').get('send_or_recv')[0] == '0' and message.get('data').get('data_type')[0] == '1' \
            :
        # and message.get('data').get('msg') == '获取key':
        logger.info('匹配成功')
        queue_recved_message.put(message)


def main():
    help(WechatPCAPI)

    wx_inst = WechatPCAPI(on_message=on_message, log=logger)
    wx_inst.start_wechat(block=True)

    while not wx_inst.get_myself():
        time.sleep(5)

    logger.info('登陆成功')
    logger.info(wx_inst.get_myself())

    time.sleep(10)

    # wx_inst.send_text(to_user='filehelper', msg='监测程序启动')
    threading.Thread(target=thread_handle_message, args=(wx_inst,)).start()


# 消息处理 分流
def thread_handle_message(wx_inst):
    while True:
        message = queue_recved_message.get()
        logger.info(message)

        try:
            msg_content = message.get('data', {}).get('msg', '')
            from_wxid = message.get('data', {}).get('from_member_wxid', '')
            from_chatroom_wxid = message.get('data', {}).get('from_chatroom_wxid', '')
            from_chatroom_nickname = message.get('data', {}).get('from_chatroom_nickname', '')
            wx_inst.send_text(from_chatroom_wxid, '微信收到群 {} 消息\n {} : {}  '.format(from_chatroom_nickname,
                                                                                   from_wxid, msg_content))
        except:
            pass


if __name__ == '__main__':
    main()
