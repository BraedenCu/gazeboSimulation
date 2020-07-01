#! /usr/bin/env python

from gazebo_msgs.srv import GetModelState
from geometry_msgs.msg import Pose
from gazeboSimulation.msg import GazeboModel
import rospy

class Zone:
    def __init__(self,state):
        self.name = state[0]
        self.types = state[1]
        self.x1 = state[2]
        self.y1 = state[3]
        self.x2 = state[4]
        self.y2 = state[5]
        self.radius = state[6]
        print(state)
    @staticmethod
    def inZone(self,model):
        if (self.types == 'rect'):
            return (self.x1 < model.pose.position.x < self.x2) & (self.y1 < model.pose.position.y < self.y2)
        elif (self.types == 'circle'):
            return (model.pose.position.x - self.x1) ** 2 + (model.pose.position.y - self.y1) ** 2 < self.radius ** 2
        else:
            print("isModelInCircle error")
            return False


def getPose(ipose):
    pose = Pose()
    pose.position.x = ipose.pose.position.x
    pose.position.y = ipose.pose.position.y
    pose.position.z = ipose.pose.position.z
    pose.orientation.x = ipose.pose.orientation.x
    pose.orientation.y = ipose.pose.orientation.y
    pose.orientation.z = ipose.pose.orientation.z
    pose.orientation.w = ipose.pose.orientation.w
    return pose

def findInArray(list, elem):
    list_row = [list.index(row) for row in list if elem in row]
    return elem[list_row]

def updateModelState(model):
    states = [
         #name           #types     #x1      #y1      #x2   #y2    #radius
        ['not_in_field', 'circle', 0      , 0     ,  0   , 0    , 100],
        ['field'       , 'rect'  , -1.82  , 1.82  ,  1.82, -1.82, 0  ],
        ['lft_top_goal', 'circle', -1.6335, 1.6335 , 0   , 0    , .05],
        ['mid_top_goal', 'circle', 0      , 1.6335 , 0   , 0    , .05],
        ['rgt_top_goal', 'circle', 1.6335 , 1.6335 , 0   , 0    , .05],

        ['lft_mid_goal', 'circle', -1.6335, 0      , 0   , 0    , .05],
        ['mid_mid_goal', 'circle', 0      , 0      , 0   , 0    , .05],
        ['rgt_mid_goal', 'circle', 1.6335 , 0      , 0   , 0    , .05],

        ['lft_dwn_goal', 'circle', -1.6335, -1.6335, 0   , 0    , .05],
        ['mid_dwn_goal', 'circle', 0      , -1.6335, 0   , 0    , .05],
        ['rgt_dwn_goal', 'circle', 1.6335 , -1.6335, 0   , 0    , .05],
    ]

    zones = [Zone]
    for state in states:
        zone = Zone(state)
        print(zone)
        zones.append(zone)

    if(model.type == 'robot'): pass
    elif(model.type == 'ball'):
        for zone in zones:
            print(zone)
            if(zone.inZone(zone,model)):
                model.state = zone.name

def main():
    # models is an array of GazeboModels
    models = [GazeboModel]

    # the initial pose is just a default pose that will change later
    initialPose = Pose()

    # intialize all the objects here. see GazeboModels.msg for more details
    objects=[
        ## four robots
        #### us
        ['robot', 'us', 'field', 'robot', 'base_link', initialPose],
        #['robot', 'us', 'field', 'robot2', 'base_link', initialPose],
        #### them
        #['robot', 'them', 'field', 'robot3', 'base_link', initialPose],
        #['robot', 'them', 'field', 'robot4', 'base_link', initialPose],

        ## balls
        #### red
        ['ball','red','field','red1', 'body',initialPose],
        ['ball','red','field','red2', 'body',initialPose],
        ['ball','red','field','red3', 'body',initialPose],
        ['ball','red','field','red4', 'body',initialPose],
        ['ball','red','field','red5', 'body',initialPose],
        ['ball','red','field','red6', 'body',initialPose],
        ['ball','red','field','red7', 'body',initialPose],
        ['ball','red','field','red8', 'body',initialPose],
        ['ball','red','field','red9', 'body',initialPose],
        ['ball','red','field','red10','body',initialPose],
        ['ball','red','field','red11','body',initialPose],
        ['ball','red','field','red12','body',initialPose],
        ['ball','red','field','red13','body',initialPose],

        #### blue
        ['ball', 'blue', 'field', 'blue1',  'body', initialPose],
        ['ball', 'blue', 'field', 'blue2',  'body', initialPose],
        ['ball', 'blue', 'field', 'blue3',  'body', initialPose],
        ['ball', 'blue', 'field', 'blue4',  'body', initialPose],
        ['ball', 'blue', 'field', 'blue5',  'body', initialPose],
        ['ball', 'blue', 'field', 'blue6',  'body', initialPose],
        ['ball', 'blue', 'field', 'blue7',  'body', initialPose],
        ['ball', 'blue', 'field', 'blue8',  'body', initialPose],
        ['ball', 'blue', 'field', 'blue9',  'body', initialPose],
        ['ball', 'blue', 'field', 'blue10', 'body', initialPose],
        ['ball', 'blue', 'field', 'blue11', 'body', initialPose],
        ['ball', 'blue', 'field', 'blue12', 'body', initialPose],
        ['ball', 'blue', 'field', 'blue13', 'body', initialPose],
    ]

    # pass objects to models
    for object in objects:
        model = GazeboModel()

        model.type =  str(object[0])
        model.spec =  str(object[1])
        model.state = str(object[2])
        model.name =  str(object[3])
        model.link =  str(object[4])
        model.pose =  object[5]
        models.append(model)

    # init ros / gazebo
    rospy.init_node('get_models_node', anonymous=True)

    # set cycles per second
    rate = rospy.Rate(10)

    # init publisher
    pub = rospy.Publisher('/gazebo/get_field', GazeboModel, queue_size=5)

    while not rospy.is_shutdown():
        try:
            # sleep
            rate.sleep()

            # wait for gazebo
            rospy.wait_for_service('/gazebo/get_model_state')

            # get updated models
            updated_models = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)
            print(updated_models)

            for model in models:
#                model.pose = getPose(updated_models(model.name, model.link))
                updateModelState(model)

        except rospy.ROSInterruptException:
            print("failed get gazebo models")

if __name__ == '__main__':
    print("get gazebo models")
    main()