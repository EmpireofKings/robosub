#!/usr/bin/env python
from flask import Flask, render_template
import rospy
from std_msgs.msg import String
import os
import sys
import rospkg
import threading
from flask_socketio import SocketIO, send, emit
#from gevent import monkey
import psutil

#monkry.patch_all()
class Sub:
    def __init__(self, name):
        self.name = name

sub = Sub('Enigma')

# This is needed in order to find templates, config and static directories due
# to how catkin handles python file installation. Since it will `exec` this 
# file from a different location, we must use the ROS API's to locate the real
# instance_path
rp = rospkg.RosPack()
app = Flask(__name__, instance_path=os.path.join(rp.get_path("webgui"), "src", "webgui"))
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)



@app.route("/")
def index():
    return render_template('index.html', sub=sub)

@app.route("/cpu")

def cpu():
    # threading.Timer(1.0,cpu).start()
    cpu_info  =  psutil.cpu_percent(interval = 0.5, percpu=True)
    return str(sum(cpu_info))



# @socketio.on('CPU_INFO')
# def refresh_cpu_usage_info():
#     while (True):
#         cpu_info  =  psutil.cpu_percent(interval = 0.5, percpu=True)
#         return sum(cpu_info)
        
# def ack():
#     print ('Massage was received')
    

# Sample callback for ROS to use
def callback(data):
    print(data.data)


def main():
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        # When running flask with debug=True, rospy has to be set up in this if
        # guard because the flask reloader forks and then calls the server, 
        # which will be killed and restarted on a reload. This causes some 
        # problems with rospy that I haven't been able to debug
        # See https://stackoverflow.com/questions/25504149/why-does-running-the-flask-dev-server-run-itself-twice
        rospy.init_node('webserver', log_level=rospy.DEBUG,  disable_signals=True)
        rospy.Subscriber('testing', String, callback)
        rospy.Subscriber("testing2", String, callback)
    # We do not need to run rospy.spin() here because all rospy.spin does is
    # block until the node is supposed to be killed
    #socketio.run(host="0.0.0.0", port = "5000", debug=True)

    
# if __name__ == '__main__':
    #socketio.run(app, debug=True)
    app.run(host="0.0.0.0", port=5000, debug=True)