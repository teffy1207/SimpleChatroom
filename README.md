# SimpleChatroom
本项目是基于TCP套接字编程的简易聊天室，用Python编写。由两部分组成：server服务器端和client客户端。server负责接收多个client建立的连接，并一直监听client的动态，若有消息传来，则将该消息发送给其他客户端。client负责发送消息。在client中还导入了Python中自带的TKinter模块，实现了简易的用户可视化聊天窗口。
