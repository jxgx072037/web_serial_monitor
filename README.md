# web_serial_monitor
基于web环境的串口调试工具

- 后台框架使用的是flask
- 串口打印通过flask-socketio实现

启动方法：
- python启动hello.py脚本后，浏览器访问127.0.0.1:5000，电机start serial!按钮，即可展示串口打印
- 关闭也面前，记得先通过http post请求关闭串口连接。post的data为json格式字符串：{"operation": "serial_close"}
