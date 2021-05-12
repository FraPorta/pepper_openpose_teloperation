import sys

from socket_receive import SocketReceive

import numpy as np

# Body parts associated to their index
body_mapping = {
    '0':  "Nose", 
    '1':  "Neck", 
    '2':  "RShoulder",
    '3':  "RElbow",
    '4':  "RWrist",
    '5':  "LShoulder",
    '6':  "LElbow",
    '7':  "LWrist",
    '8':  "MidHip"
    }

## function vector_from_points
#
# calculate 3D vector from two points ( vector = P2 - P1 )
def vector_from_points(P1, P2):
    vector = [P2[0] - P1[0], P2[1] - P1[1], P2[2] - P1[2]]
    return vector

## function obtain_LShoulderPitchRoll_angles
# 
# Calculate left shoulder pitch and roll angles
def obtain_LShoulderPitchRoll_angles(P1, P5, P6, P8):
    # Construct 3D vectors (bones) from points
    v_1_5 = vector_from_points(P1, P5)
    v_5_1 = vector_from_points(P5, P1)
    v_6_5 = vector_from_points(P6, P5)
    v_5_6 = vector_from_points(P5, P6)

    # # Calculate normal of the 1_5_6 plane
    # n_1_5_6 = np.cross(v_1_5, v_6_5)

    # Left torso Z axis
    v_8_1 = vector_from_points(P8, P1)

    # Left torso X axis 
    n_8_1_5 = np.cross(v_8_1, v_5_1)

    # Left torso Y axis
    R_left_torso = np.cross(v_8_1, n_8_1_5)

    # Intermediate angle to calculate positive or negative final Pitch angle
    intermediate_angle = np.arccos(np.dot(v_5_6, v_8_1) / (np.linalg.norm(v_5_6))*(np.linalg.norm(v_8_1)))
    
    # Module of the LShoulderPitch angle
    theta_LSP_module = np.arccos(np.dot(v_8_1, np.cross(R_left_torso, v_5_6))/(np.linalg.norm(v_8_1) * np.linalg.norm(np.cross(R_left_torso, v_5_6))))

    # Positive or negative LShoulderPitch
    if intermediate_angle <= np.pi/2 :
        LShoulderPitch = -theta_LSP_module
    else:
        LShoulderPitch = theta_LSP_module

    # Formula for LShoulderRoll
    LShoulderRoll = (np.pi/2) - np.arccos((np.dot(v_5_6, R_left_torso)) / (np.linalg.norm(v_5_6) * np.linalg.norm(R_left_torso)))

    # Return LShoulder angles
    return LShoulderPitch, LShoulderRoll

## function obtain_LElbowYawRoll_angle
# 
# Calculate left elbow yaw and roll angles
def obtain_LElbowYawRoll_angle(P1, P5, P6, P7):
    # Construct 3D vectors (bones) from points
    v_6_7 = vector_from_points(P6, P7)
    v_1_5 = vector_from_points(P1, P5)

    # Left arm Z axis
    v_6_5 = vector_from_points(P6, P5)
    # Left arm X axis
    n_1_5_6 = np.cross(v_1_5, v_6_5)
    # Left arm Y axis
    R_left_arm = np.cross(v_6_5, n_1_5_6)

    # Normal of 5_6_7 plane
    n_5_6_7 = np.cross(v_6_5, v_6_7) 

    # Formula to calculate the module of LElbowYaw angle
    theta_LEY_module = np.arccos(np.dot(n_1_5_6, n_5_6_7) / (np.linalg.norm(n_1_5_6) * np.linalg.norm(n_5_6_7)))

    # Intermediate angles to choose the right LElbowYaw angle
    intermediate_angle_1 = np.arccos(np.dot(v_6_7, n_1_5_6) / (np.linalg.norm(v_6_7) * np.linalg.norm(n_1_5_6)))
    intermediate_angle_2 = np.arccos(np.dot(v_6_7, R_left_arm) / (np.linalg.norm(v_6_7) * np.linalg.norm(R_left_arm)))

    # Choice of the correct LElbowYaw angle using intermediate angles values
    if intermediate_angle_1 <= np.pi/2:
        LElbowYaw = -theta_LEY_module
    elif intermediate_angle_2 > np.pi/2:
        LElbowYaw = theta_LEY_module
    elif intermediate_angle_2 <= np.pi/2:
        LElbowYaw = theta_LEY_module - 2 * np.pi

    # Formula for LElbowRoll angle
    LElbowRoll = np.pi - np.arccos(np.dot(v_6_7, v_6_5) / (np.linalg.norm(v_6_7) * np.linalg.norm(v_6_5)))

    # Return LElbow angles
    return LElbowYaw, LElbowRoll

def obtain_RShoulderPitchRoll_angle(P1, P2, P3, P8):
    # Construct 3D vectors (bones) from points
    v_2_3 = vector_from_points(P2, P3)
    v_1_2 = vector_from_points(P1, P2)
    v_2_1 = vector_from_points(P2, P1)

    # Right torso Z axis
    v_8_1 = vector_from_points(P8, P1)
    # Right torso X axis
    n_8_1_2 = np.cross(v_8_1, v_1_2)
    # Right torso Y axis
    R_right_torso = np.cross(v_8_1, n_8_1_2)

    # # Normal to plane 1_2_3
    # n_1_2_3 = np.cross(v_2_3, v_2_1)

    # Module of the RShoulderPitch angle
    theta_RSP_module = np.arccos(np.dot(v_8_1, np.cross(R_right_torso, v_2_3))/(np.linalg.norm(v_8_1) * np.linalg.norm(np.cross(R_right_torso, v_2_3))))
    
    # Intermediate angle to calculate positive or negative final Pitch angle
    intermediate_angle = np.arccos(np.dot(v_2_3, v_8_1) / (np.linalg.norm(v_2_3))*(np.linalg.norm(v_8_1)))

    # Positive or negative RShoulderPitch
    if intermediate_angle <= np.pi/2 :
        RShoulderPitch = - theta_RSP_module
    else:
        RShoulderPitch = theta_RSP_module

    # Formula for RShoulderRoll
    RShoulderRoll = np.arccos((np.dot(v_2_3, R_right_torso)) / (np.linalg.norm(v_2_3) * np.linalg.norm(R_right_torso))) - (np.pi/2)

    # Return RShoulder angles
    return RShoulderPitch, RShoulderRoll

def obtain_RElbowYawRoll_angle(P1, P2, P3, P4):
    # Construct 3D vectors (bones) from points
    v_3_4 = vector_from_points(P3, P4)
    v_1_2 = vector_from_points(P1, P2)
    v_2_3 = vector_from_points(P2, P3)

    # Left arm Z axis
    v_3_2 = vector_from_points(P3, P2)
    # Left arm X axis
    n_1_2_3 = np.cross(v_3_2, v_1_2)
    # Left arm Y axis
    R_right_arm = np.cross(v_3_2, n_1_2_3)

    # normal to the 2_3_4 plane
    n_2_3_4 = np.cross(v_3_2, v_3_4)

    # Formula to calculate the module of RElbowYaw angle
    theta_REY_module = np.arccos(np.dot(n_1_2_3, n_2_3_4) / (np.linalg.norm(n_1_2_3) * np.linalg.norm(n_2_3_4)))

    # Intermediate angles to choose the right RElbowYaw angle
    intermediate_angle_1 = np.arccos(np.dot(v_3_4, n_1_2_3) / (np.linalg.norm(v_3_4) * np.linalg.norm(n_1_2_3)))
    intermediate_angle_2 = np.arccos(np.dot(v_3_4, R_right_arm) / (np.linalg.norm(v_3_4) * np.linalg.norm(R_right_arm)))

    # Choice of the correct RElbowYaw angle using intermediate angles values
    if intermediate_angle_1 <= np.pi/2:
        RElbowYaw = -theta_REY_module

    elif intermediate_angle_2 > np.pi/2:
        RElbowYaw = theta_REY_module

    elif intermediate_angle_2 <= np.pi/2:
        RElbowYaw = theta_REY_module - 2 * np.pi

    # Formula for RElbowRoll angle
    RElbowRoll = np.pi - np.arccos(np.dot(v_3_4, v_3_2) / (np.linalg.norm(v_3_4) * np.linalg.norm(v_3_2)))

    # Return RElbow angles
    return RElbowYaw, RElbowRoll

## function invert_right_left
#
# Invert left and right arm
def invert_right_left(wp_dict):
    temp_dict = wp_dict
    if '2' in wp_dict:
        temp_dict['5']=wp_dict['2']
    if '3' in wp_dict:
        temp_dict['6']=wp_dict['3']
    if '4' in wp_dict:
        temp_dict['7']=wp_dict['4']
    if '5' in wp_dict:
        temp_dict['2']=wp_dict['5']
    if '6' in wp_dict:
        temp_dict['3']=wp_dict['6']
    if '7' in wp_dict:
        temp_dict['4']=wp_dict['7']
    return temp_dict

try:
    # Init dictionary
    wp_dict = {}

    # initialize socket for receiving the 3D keypoints
    sr = SocketReceive()

    # LShoulderPitch and LShoulderRoll needed keypoints
    LS = ['1','5','6','8']

    # LElbowYaw and LElbowRoll needed keypoints
    LE = ['1','5','6','7']

    # RShoulderPitch and RShoulderRoll needed keypoints
    RS = ['1','2','3','8']

    # RElbowYaw and RElbowRoll needed keypoints
    RE = ['1','2','3','4']   

    print("Start receiving keypoints...")
    while True:
        # Receive keypoints from socket
        wp_dict = sr.receive_keypoints()
        # print(wp_dict)
        wp_dict = invert_right_left(wp_dict)

        # LShoulder angles (Green arm on OpenPose)
        if all (body_part in wp_dict for body_part in LS):        
            LShoulderPitch, LShoulderRoll = obtain_LShoulderPitchRoll_angles(wp_dict.get(LS[0]), wp_dict.get(LS[1]), wp_dict.get(LS[2]), wp_dict.get(LS[3]))

            # # Print angles
            # print("LShoulderPitch:")
            # print((LShoulderPitch * 180 )/ np.pi)

            # print("LShoulderRoll:")
            # print((LShoulderRoll * 180)/ np.pi)

        # LElbow angles (Green arm on OpenPose)
        if all (body_part in wp_dict for body_part in LE):
            LElbowYaw, LElbowRoll = obtain_LElbowYawRoll_angle(wp_dict.get(LE[0]), wp_dict.get(LE[1]), wp_dict.get(LE[2]), wp_dict.get(LE[3]))

            # Print angles
            print("LElbowYaw:")
            # print((LElbowYaw * 180 )/ np.pi)
            print(LElbowYaw)

            print("LElbowRoll:")
            # print((LElbowRoll * 180)/ np.pi)
            print(LElbowRoll)

        # RShoulder angles
        if all (body_part in wp_dict for body_part in RS):        
            RShoulderPitch, RShoulderRoll = obtain_RShoulderPitchRoll_angle(wp_dict.get(RS[0]), wp_dict.get(RS[1]), wp_dict.get(RS[2]), wp_dict.get(RS[3]))

            # # Print angles
            # print("RShoulderPitch:")
            # print((RShoulderPitch * 180 )/ np.pi)

            # print("RShoulderRoll:")
            # print((RShoulderRoll * 180)/ np.pi)


        # # RElbow angles
        if all (body_part in wp_dict for body_part in RE):
            RElbowYaw, RElbowRoll = obtain_RElbowYawRoll_angle(wp_dict.get(RE[0]), wp_dict.get(RE[1]), wp_dict.get(RE[2]), wp_dict.get(RE[3]))
            
            # # Print angles
            # print("RElbowYaw:")
            # print((RElbowYaw * 180 )/ np.pi)

            # print("RElbowRoll:")
            # print((RElbowRoll * 180)/ np.pi)

except Exception as e:
    print(e)
    exc_type, exc_obj, exc_tb = sys.exc_info()
    print(exc_type, exc_tb.tb_lineno)
    sys.exit(-1)