import socket
import  time


def main():
    # 1、创建一个udp套接字
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        # 从键盘获取数据
        # send_data = input("请输入chongfu发送内容：")
        send_data = "hello world"
        # 判断结束
        if send_data == "exit":
            break
        # 使用套接字收发数据
        udp_socket.sendto(send_data.encode("GB2312"), ("192.168.100.68", 8080))
        time.sleep(0.01)
    # 5、关闭套接字
    udp_socket.close()


if __name__ == "__main__":
    main()