#!/usr/bin/env python
# This is needed in order to find templates, config and static directories due
# to how catkin handles python file installation. Since it will `exec` this 
# file from a different location, we must use the ROS API's to locate the real
# instance_path
import rospkg, sys, os
rp = rospkg.RosPack()
path = os.path.join(rp.get_path("webgui"), "src", "webgui")
sys.path.insert(0, path)

from flask import Flask, render_template
import rospy
from std_msgs.msg import String
import threading
import config



class Sub:
    def __init__(self, name):
        self.name = name

sub = Sub('Enigma')
app = Flask(__name__, instance_path=path)

@app.route("/")
def index():
    return render_template('index.html', sub=sub)

# Sample callback for ROS to use
def callback(data):
    print(data.data)


def main():
    # Check if we are doing an autonomous run. If so, the web gui should not be
    # running as it is just a waste of resources
    try:
        mode = rospy.get_param('/mode')
        if mode == 'autonomous':
            # Don't run the gui on an autonomous run
            print("Running in autonomous mode. Web GUI is not needed")
            return
    except KeyError:
        pass

    app.config.from_object('config.DevelopmentConfig')
    if (not app.config['DEBUG']) or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        # When running flask with debug=True, rospy has to be set up in this if
        # guard because the flask reloader forks and then calls the server, 
        # which will be killed and restarted on a reload. This causes some 
        # problems with rospy that I haven't been able to debug
        # See https://stackoverflow.com/questions/25504149/why-does-running-the-flask-dev-server-run-itself-twice
        rospy.init_node('webserver', log_level=rospy.DEBUG,  disable_signals=True)
        rospy.Subscriber('testing', String, callback)

    # We do not need to run rospy.spin() here because all rospy.spin does is
    # block until the node is supposed to be killed
    app.run(host="0.0.0.0")
