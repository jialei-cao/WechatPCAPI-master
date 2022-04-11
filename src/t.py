def main():
    message = {'user': 'wxid_k1mp1p792r3y22', 'type': 'msg::chatroom', 'data': {'data_type': '1', 'send_or_recv': '0+[收到]', 'from_chatroom_wxid': '18322509606@chatroom', 'from_member_wxid': 'wxid_hjbvmparqynk22', 'time': '2022-03-29 15:17:51', 'msg': '12345', 'msg_byte_hex': '3132333435', 'from_chatroom_nickname': '群聊测试'}}

    print(message.get('data').get('data_type')[0])
    print(message.get('type') == 'msg::chatroom' and message.get('data').get('from_chatroom_nickname') == '群聊测试' \
          and message.get('data').get('send_or_recv')[0] == '0' and message.get('data').get('data_type')[0] == '1')

if __name__ == '__main__':
    main()
