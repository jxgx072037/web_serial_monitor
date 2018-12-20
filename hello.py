from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

import serial
from serial.tools.list_ports import get_ports_list  #用我们自己改过的list_ports获取windows上可用的串口

async_mode = None

app = Flask(__name__, template_folder='./')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)

close_mark = False

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        return render_template('serial_test.html', async_mode=socketio.async_mode)
    if request.method == "POST":  # 使用http post方式停掉串口
        ser = serial.Serial()
        ser.baudrate = 115200
        ser.port = (get_ports_list()[0][0])
        ser.xonxoff = True

        global serial_port
        serial_port = ser.port
        ser.close()

        global close_mark
        close_mark = True
        print("serial port %s is closed" % serial_port)


        # os._exit(0)  # 关闭服务器

        return "serial port %s is closed" % serial_port

@socketio.on('serial_open', namespace='/serial')
def serial_open(message):

    global close_mark
    close_mark = False

    # 定义串口参数
    ser = serial.Serial()
    ser.baudrate = 115200
    ser.xonxoff = True

    try:
        ser.port = (get_ports_list()[0][0])
    except:
        print ("There is no serial port, please check hardware connection.")
        return

    global serial_port
    serial_port = ser.port

    # 开启串口
    ser.open()

    while close_mark == False:
        check_mark = []
        content_read = ser.read(50).decode("utf-8", "ignore").split("\r\n")
        for index in range(0, len(content_read)):
            check_mark.append(len(content_read[index].strip()))

        index_output = check_mark.index(max(check_mark))
        content_output = content_read[index_output].strip()

        emit('my_response', {'data': content_output})

    ser.close()

if __name__ == '__main__':
    socketio.run(app)