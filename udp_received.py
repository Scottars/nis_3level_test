from socket import *





def main():
    package_cnt = 0
    # 1、创建一个udp套接字
    udp_socket = socket(AF_INET, SOCK_DGRAM)
    # 2、绑定本地相关信息，如果不绑定，则随机分配
    local_addr = ('', 8080)  # ip地址和端口号，IP不写表示本机任何一个ip
    udp_socket.bind(local_addr)
    # 3、等待接收对方发送的数据
    while True:
        recv_data = udp_socket.recvfrom(1024)  # 1024表示本次接收的最大字节
        package_cnt = package_cnt +1
        if package_cnt==1000000:
            break

        # recv_data存储的是一个元组（发送方ip，Port）
        recv_msg = recv_data[0]
        send_addr = recv_data[1]
        print(package_cnt)
        # 4、显示接收到的数据
        # print("%s:%s" % (str(send_addr), recv_msg.decode("gbk")))
    udp_socket.close()


if __name__ == "__main__":
    main()













