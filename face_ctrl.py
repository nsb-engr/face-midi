
# This code was written with reference to the snippet from
#   https://google.github.io/mediapipe/solutions/face_mesh


from enum import IntEnum
import argparse
import cv2
import mediapipe as mp

import drawing_utils
from indicators import draw_meter
from midi_utils import MIDIControl
from set_midi_port import set_midi_port
import config as cfg

mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

my_drawing = drawing_utils

HIDE_FACE = False

class Face(IntEnum):
    TOP = 10
    U_LIP = 13
    D_LIP = 14
    L_LIP = 78
    R_LIP = 308
    #BOTTOM = 152


def _hide_face(image, v_bottom:tuple, v_top:tuple=(0,0)):
  x0, y0 = v_top
  x1, y1 = v_bottom
  pt1 = (x1-100, max(0,y0-40))
  pt2 = (x1+100, y1-10)
  cv2.rectangle(image, pt1, pt2,
                color=(100,100,100),thickness=-1,
                lineType=cv2.LINE_4)


def _normalize(aperture, max_, min_):
    coef = 127.0 / (max_ - min_)
    aperture = coef * (aperture - min_)

    if aperture > 127:
        aperture = 127
    if aperture < 0:
        aperture = 0
        
    return int(aperture)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ch', type=int, default=0, help="MIDI ch")
    parser.add_argument('--ctrl', type=int, default=80, help="Control Change No.")
    parser.add_argument('--cam_id', type=int, default=0, help="OpenCV Camera ID")
    args = parser.parse_args()

    cap = cv2.VideoCapture(args.cam_id, cv2.CAP_DSHOW)
    if not cap.isOpened():
        raise IOError("Can't open a camera device")

    cap.set(cv2.CAP_PROP_BUFFERSIZE,2)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720)
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
    # cap.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'YUYV'))

    # Add line to write on a face
    connections = set(mp_face_mesh.FACE_CONNECTIONS)
    connections.add((13,14)) # Vertical line from upper lip to lower lip
    #connections.add((78,308)) # Horizontal line crossing the mouth

    max_ = 10
    min_ = 0

    midi_ctl = MIDIControl()

    if cfg.PORTNAME == None:
        set_midi_port()
    midi_ctl.open_output(cfg.PORTNAME)

    with mp_face_mesh.FaceMesh(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as face_mesh:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                continue

            # Flip the image horizontally for a later selfie-view display, and convert
            # the BGR image to RGB.
            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            results = face_mesh.process(image)

            # Draw the face mesh annotations on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            aperture = 1e-9
            if results.multi_face_landmarks:
                face_landmarks = results.multi_face_landmarks[0]
                idx_to_coordinates = my_drawing.draw_landmarks(
                                    image=image,
                                    landmark_list=face_landmarks,
                                    connections=connections,
                                    landmark_drawing_spec=drawing_spec,
                                    connection_drawing_spec=drawing_spec)
                #print({key for key in Face})
                #print(idx_to_coordinates)
                if idx_to_coordinates.keys() >= {Face.U_LIP, Face.D_LIP}:
                    # face_length = idx_to_coordinates[Face.BOTTOM][1] - idx_to_coordinates[Face.TOP][1] 
                    aperture = (idx_to_coordinates[Face.D_LIP][1] - idx_to_coordinates[Face.U_LIP][1])
                    if Face.TOP not in  idx_to_coordinates:
                        idx_to_coordinates[Face.TOP] = (0,0)

                    if HIDE_FACE:
                        _hide_face(image,
                                    idx_to_coordinates[Face.U_LIP],
                                    idx_to_coordinates[Face.TOP])
            
            n_aperture = _normalize(aperture, max_, min_)
            draw_meter(image, n_aperture)

            midi_ctl.send_control_change(
                                    args.ch,
                                    args.ctrl,
                                    n_aperture)

            cv2.imshow('MediaPipe FaceMesh', image)
            key = cv2.waitKey(5) & 0xFF
            if  key == 27:
                break

            #calibration
            ## set current value as max
            elif key == ord("u") and aperture > min_:
                max_ = aperture
            ## set current value as min
            elif key == ord("d") and aperture < max_:
                min_ = aperture

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()