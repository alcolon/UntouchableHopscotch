#!/usr/bin/env python

import rospy
import math
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion

def odom_cb(msg):
    global x, y, z
    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y

    global roll, pitch, yaw
    orientation_q = msg.pose.pose.orientation
    orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
    (roll, pitch, yaw) = euler_from_quaternion (orientation_list)



rospy.init_node('cpu')
cpub = rospy.Publisher('/cpu/cmd_vel', Twist, queue_size=1)
t = Twist()
cpsub = rospy.Subscriber('cpu/odom', Odometry, odom_cb)
rate = rospy.Rate(2)




#------------------VARIABLES---------------------
current = "2"
location = [0,0]
goal = [4,5]

states = {  0 : "starting",
            1 : "white",
            2 : "black",
            3 : "goal"}

direction = {"up" : 1,
            "right" : 2}


gameboard8 = {  (2, 1, 1, 2, 2, 1, 1, 2), # 1.75  y values
                (1, 2, 2, 1, 2, 1, 2, 2), # 1.25
                (1, 2, 2, 1, 2, 2, 2, 1), # .75
                (1, 2, 1, 1, 1, 1, 1, 2), # .25
                (1, 1, 2, 2, 3, 1, 2, 1), # -.25
                (2, 1, 2, 1, 2, 1, 2, 1), # -.75
                (1, 1, 1, 1, 2, 1, 1, 1), # -1.25
                (0, 2, 1, 2, 1, 2, 1, 1)} # -1.75
             #  -1.70 -1.20 -.70 -.20 .30 .80 1.30 1.80  .5 offset due to robot's root being off center
             # x values
             # distance between consecutive squares = +/-.45





def permission(way):
    if (way == "1"):
        if (gameboard([location[0] + 1][location[1]] == 2 or location[0] != 0)):
                return True
        elif (way == "2"):
            if (gameboard([location[1] - 1][location[1]] == 2 or location[0] != 7)):
                return True

        else:
            return False

x = 0
y = 0
roll = pitch = yaw = 0
target_angle = 90
distance_to_drive = .5 #meters
kP = .5

#-----------buffer------------ waiting for odom

# while x is 0:
#     rate.sleep()

#-----------------------------
def where_am_i():
    return location

# NOTE: improvements:   i could replace this with one method! replace with boolean
#                       implement a more efficient turn system

# -----------------DIRECTIONS-----------------------------
def up(): #moves into next box
    target_angle = 0
    x_old = x
    target_rad = target_angle * math.pi/180
    while(yaw != 0):
        t.angular.z = kP  * (target_rad - yaw)
        cpub.publish(t)
    t.linear.x = .6
    cpub.publish(t)
    # while (x - x_old <= distance_to_drive):
    #     t.linear.x = .3
    #     cpub.publish(t)
    # t.linear.x =  0
    # cpub.publish(t)
    # location[0] += 1 # updating location

def right():
    target_angle = 90
    x_old = x
    target_rad = target_angle * math.pi/180
    while(yaw != target_rad):
        t.angular.z = kP  * (target_rad - yaw)
        cpub.publish(t)
    t.angular.z = 0
    cpub.publish(t)
    while (x - x_old <= distance_to_drive):
        t.linear.x = .3
        cpub.publish(t)
    t.linear.x =  0
    cpub.publish(t)
    location[0] += 1 # updating location

def stop():
    t.angular.z = 0
    t.linear.x = 0
    cpub.publish(t)

def algorithm():
    if (goal[0]-location[0] >= goal[1]-location[1]):
        if (permission(1)):
            up()
        elif (permission(2)):
            right()
        else:
            stop()


while not rospy.is_shutdown():
    print("whatido")
    # t.linear.x =.2
    # cpub.publish(t)
    up()
    # stop()
    # print("star")
    # right()
    rate.sleep()

    # down()
    # left()
    # right()
    # if (location == location_old):
    #     print("success!")
    # else:
    #     print("check your values :/")
