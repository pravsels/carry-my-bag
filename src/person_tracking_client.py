#!/usr/bin/env python2
import rospy
from tiago import Tiago
from person_follower import PersonFollower
from smach import StateMachine
from states.TakeBag import TakeBag
from states.StandBy import StandBy
from states.Follow import Follow

if __name__ == '__main__':
    rospy.init_node('porter')
    tiago = Tiago()
    follower = PersonFollower('')
    tiago.go_to_conf_room()

    sm = StateMachine(outcomes=['success', 'failure'])  # the end states of the machine
    with sm:

        StateMachine.add('stand_by', StandBy(tiago, follower), transitions={'porter_request': 'take_bag', 'loop_back': 'stand_by'})
        StateMachine.add('take_bag', TakeBag(tiago, follower), transitions={'start_following': 'follow', 'nothing_given': 'take_bag'})
        StateMachine.add('follow', Follow(tiago, follower), transitions={'follow_done': 'success', 'still_following': 'follow'})

        sm.execute()

    rospy.spin()
