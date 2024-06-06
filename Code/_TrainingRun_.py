import tkinter as tk
from tkinter.messagebox import showerror
from idlelib.tooltip import Hovertip

import logging
import _defs_
from _DataBaseInfo_ import DataBaseInfo

import cv2
import mediapipe as mp
from PIL import Image, ImageTk
from math import atan2, degrees, pi

import os
# from playsound import playsound

class TrainingRun(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.cameraClass = _defs_.CameraUsage()
        self.yogaObject = _defs_.YOGAINFO()

        _defs_.setBackgroundImage(self, _defs_.getSpecialBckgndPicture())

        buttonHeight, buttonWidth = _defs_.getStandartButtonSize()
        self.canvasWidth, self.canvasHeight = 600, 400

        self.mp_drawing = mp.solutions.drawing_utils
        self.poses = []
        #self.mp_poses = []
        #self.mp_poses.append(mp.solutions.pose)
        #self.mp_poses.append(mp.solutions.pose)
        self.mp_poses = mp.solutions.pose
        # camera poses
        self.poses.append(self.mp_poses.Pose(
            #static_image_mode=True,
            static_image_mode=False,
            model_complexity=0,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5))
        # photo poses
        self.poses.append(self.mp_poses.Pose(
            static_image_mode=True,
            model_complexity=0,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5))

        #self.cameraID = _defs_.getCameraID() --old
        self.cameraID = self.cameraClass.returnSelectedCameraID()

        self.isBroken = False # if camera's broken
        self.successfuly_released = False

        self.iterNumber = 0
        self.RESULTING_SCORE = 0
        self.CURRENT_SCORE = 0

        self.MAX_TIME = 30
        self.remainingTime = self.MAX_TIME
        self.full_path = _defs_.getStandartPath() + "full_timer" + str(self.MAX_TIME) + _defs_.get_MP3()
        self.half_path = _defs_.getStandartPath() + "half_timer" + str(int(self.MAX_TIME / 2)) + _defs_.get_MP3()

        self.isExpired = False

        self.infoLabel = tk.Label(self, text="Ожидаем", bg=_defs_.getWidgetColor(), font=20)

        #self.timeLabel = tk.Label(self, text="Осталось времени: " + str(self.MAX_TIME), bg=_defs_.getWidgetColor())

        self.progressTimerCanvas = tk.Canvas(self, width=100, height=100,  bg=_defs_.getWidgetColor())
        self.timer_label = self.progressTimerCanvas.create_text(50, 50, text=str(self.remainingTime), font=('Arial', 20))

        self.errorCameraButton = tk.Button(self, text="Экстренный выход",  height= buttonHeight, width= buttonWidth,
                                           state = tk.DISABLED, command=lambda: self.emergencyExit())
        tip_errorCameraButton = Hovertip(self.errorCameraButton, 'Нужна на случай проблемы с камерой')

        #self.yogaPicture = cv2.imread(getStandartPath()+"yoga5.png")
        self.yogaPicture = cv2.imread(_defs_.getStandartPath()+self.yogaObject.getCurrentElementFromYoga()+_defs_.get_PNG())

        self.cameraCanvas = tk.Canvas(self, width=self.canvasWidth, height=self.canvasHeight)
        self.photoCanvas = tk.Canvas(self, width=self.canvasWidth, height=self.canvasHeight)
        self.itsOkay = False

        self.infoLabel.pack(side=tk.TOP, pady = 30)
        self.errorCameraButton.pack(side=tk.BOTTOM, pady=30)
        #self.timeLabel.pack(side=tk.BOTTOM, pady=10)
        self.progressTimerCanvas.pack(side=tk.BOTTOM, pady=10)
        self.cameraCanvas.pack(side=tk.LEFT, padx = 20)
        self.photoCanvas.pack(side=tk.RIGHT, padx = 20)


    def get_landmark_name(self, index):
        if index == 0:
            return "nose"
        elif index == 1:
            return "right eye inner"
        elif index == 2:
            return "right eye"
        elif index == 3:
            return "right eye outer"
        elif index == 4:
            return "left eye inner"
        elif index == 5:
            return "left eye"
        elif index == 6:
            return "left eye outer"
        elif index == 7:
            return "right ear"
        elif index == 8:
            return "left ear"
        elif index == 9:
            return "mouth right"
        elif index == 10:
            return "mouth left"
        elif index == 11:
            return "right shoulder"
        elif index == 12:
            return "left shoulder"
        elif index == 13:
            return "right elbow"
        elif index == 14:
            return "left elbow"
        elif index == 15:
            return "right wrist"
        elif index == 16:
            return "left wrist"
        elif index == 17:
            return "right pinky knuckle"
        elif index == 18:
            return "left pinky knuckle"
        elif index == 19:
            return "right index knuckle"
        elif index == 20:
            return "left index knuckle"
        elif index == 21:
            return "right thumb knuckle"
        elif index == 22:
            return "left thumb knuckle"
        elif index == 23:
            return "right hip"
        elif index == 24:
            return "left hip"
        elif index == 25:
            return "right knee"
        elif index == 26:
            return "left knee"
        elif index == 27:
            return "right ankle"
        elif index == 28:
            return "left ankle"
        elif index == 29:
            return "right heel"
        elif index == 30:
            return "left heel"
        elif index == 31:
            return "right foot"
        elif index == 32:
            return "left foot"


    def get_middle_points(self, right, left):
        dx = abs(right.x - left.x)
        dy = abs(right.y - left.y)
        middle_x = min(right.x, left.x) + dx / 2
        middle_y = min(right.y, left.y) + dy / 2
        return middle_x, middle_y


    def get_definition_landmarks(self, landmarks):
        definition_landmarks = []
        definition_landmarks.append(landmarks[11])
        definition_landmarks.append(landmarks[12])
        definition_landmarks.append(landmarks[23])
        definition_landmarks.append(landmarks[24])
        return definition_landmarks


    def get_anchor_points(self, frame, landmarks):
        middle_landmark_shoulders_x, middle_landmark_shoulders_y = self.get_middle_points(landmarks[0], landmarks[1])
        middle_landmark_hips_x, middle_landmark_hips_y = self.get_middle_points(landmarks[2], landmarks[3])

        start_point_shoulders = (int(landmarks[0].x * frame.shape[1]), int(landmarks[0].y * frame.shape[0]))
        end_point_shoulders = (int(landmarks[1].x * frame.shape[1]), int(landmarks[1].y * frame.shape[0]))

        start_point_hips = (int(landmarks[2].x * frame.shape[1]), int(landmarks[2].y * frame.shape[0]))
        end_point_hips = (int(landmarks[3].x * frame.shape[1]), int(landmarks[3].y * frame.shape[0]))

        start_point_middle = (int(middle_landmark_shoulders_x * frame.shape[1]), int(middle_landmark_shoulders_y * frame.shape[0]))
        end_point_middle = (int(middle_landmark_hips_x * frame.shape[1]), int(middle_landmark_hips_y * frame.shape[0]))

        thickness_ = 3
        # linetype_ = cv2.LINE_AA
        linetype_ = cv2.LINE_4
        cv2.line(frame, start_point_middle, end_point_middle, (0, 255, 0), thickness=thickness_, lineType=linetype_)
        cv2.line(frame, start_point_shoulders, end_point_shoulders, (0, 255, 0), thickness=thickness_,
                 lineType=linetype_)
        cv2.line(frame, start_point_hips, end_point_hips, (0, 255, 0), thickness=thickness_, lineType=linetype_)

        return (start_point_middle, end_point_middle)


    def points_degrees(self, point1, point2):
        dx = point1[0] - point2[0]
        dy = point1[1] - point2[1]
        rads = atan2(-dy, dx)
        rads %= 2 * pi
        return degrees(rads)


    # rewrite the code to avoid the problem with pose estimator !!!
    def highlight_mismatch(self, frame1, frame2, landmarks1, landmarks2):
        MAX_NUM_LANDMARKS = 33  # 0 - nose , ... , 32 - left foot index
        # see at https://developers.google.com/mediapipe/solutions/vision/pose_landmarker

        # right shoulder = 11
        # left  shoulder = 12
        # right hip      = 23
        # left  hip      = 24

        # start_time = time.time()
        def_lm_1 = self.get_definition_landmarks(landmarks1)  # get lm: shoulders, hips
        base_points1 = self.get_anchor_points(frame1, def_lm_1)

        # print("---EXEC TIME:  %s seconds ---" % (time.time() - start_time))

        compared_angle = 15

        excludedPoints = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 17, 18, 19, 20, 21, 22]

        EXCLUDED_POINTS_NUMBER = len(excludedPoints)

        cv2.putText(frame1, "Highlighted RED:", (10, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
        y_offset = 20
        rightPoints = 0
        for i, (lm1, lm2) in enumerate(zip(landmarks1, landmarks2)):
            #if (i not in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 17, 18, 19, 20, 21, 22)):  # not needed
            if (i not in excludedPoints):  # not needed
                if lm1.visibility and lm2.visibility:
                    shapes_lm1 = (int(lm1.x * frame1.shape[1]), int(lm1.y * frame1.shape[0]))
                    shapes_lm2 = (int(lm2.x * frame2.shape[1]), int(lm2.y * frame2.shape[0]))

                    lm1_shoulders_degrees = abs(self.points_degrees(base_points1[0], shapes_lm1))
                    lm2_shoulders_degrees = abs(self.points_degrees(base_points2[0], shapes_lm2))

                    lm1_hips_degrees = abs(self.points_degrees(base_points1[1], shapes_lm1))
                    lm2_hips_degrees = abs(self.points_degrees(base_points2[1], shapes_lm2))

                    shoulders_degrees, hips_degrees = 0, 0

                    if (((lm1_shoulders_degrees > 180 and lm2_shoulders_degrees < 180) or (
                            lm1_shoulders_degrees < 180 and lm2_shoulders_degrees > 180))
                            and (lm1_shoulders_degrees + lm2_shoulders_degrees > 360)):
                        shoulders_degrees = lm1_shoulders_degrees + lm2_shoulders_degrees - 360
                    else:
                        shoulders_degrees = abs(lm1_shoulders_degrees - lm2_shoulders_degrees)

                    if (((lm1_hips_degrees > 180 and lm2_hips_degrees < 180) or (
                            lm1_hips_degrees < 180 and lm2_hips_degrees > 180))
                            and (lm1_hips_degrees + lm2_hips_degrees > 360)):
                        hips_degrees = lm1_hips_degrees + lm2_hips_degrees - 360
                    else:
                        hips_degrees = abs(lm1_hips_degrees - lm2_hips_degrees)

                    if ((i <= 22) and (shoulders_degrees > compared_angle)) or (
                            (i > 22) and (hips_degrees > compared_angle)):  # compare shoulders
                        rightPoints += 1
                        #cv2.circle(frame1, shapes_lm1, 3, (255, 0, 0), -1)
                        cv2.circle(frame1, shapes_lm1, 12, (255, 0, 0), 4)
                        #cv2.circle(frame1, shapes_lm1, 12, (0, 0, 0), 4)
                        cv2.putText(frame1, "- " + self.get_landmark_name(i), (10, 10 + y_offset),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.25, (255, 255, 255), 1)
                        # cv2.putText(frame1, f"Index: {i}, Distance: {distance:.2f}", (10, 10 + y_offset),
                        #            cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255), 1)
                        y_offset += 7
        y_offset += 20

        currentSCORE = int(((MAX_NUM_LANDMARKS - EXCLUDED_POINTS_NUMBER - rightPoints) / (MAX_NUM_LANDMARKS - EXCLUDED_POINTS_NUMBER)) * 100)
        self.iterNumber += 1
        self.CURRENT_SCORE += currentSCORE

        self.infoLabel.config(text="РЕКОРД: " + str(currentSCORE) + " %")
        cv2.putText(frame1, "SCORE: " + str(currentSCORE) + " %", (10, 10 + y_offset),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)


    def exercise_handler(self):
        global frame2, results2, base_points2
        frame2 = cv2.cvtColor(self.yogaPicture, cv2.COLOR_BGR2RGB)
        frame2 = cv2.resize(frame2, (self.canvasWidth, self.canvasHeight))
        results2 = self.poses[1].process(frame2)

        if results2.pose_landmarks:
            self.mp_drawing.draw_landmarks(frame2, results2.pose_landmarks, self.mp_poses.POSE_CONNECTIONS)

        def_lm_2 = self.get_definition_landmarks(results2.pose_landmarks.landmark)  # get lm: shoulders, hips
        base_points2 = self.get_anchor_points(frame2, def_lm_2)


    #def update_label(self):
    #    self.timeLabel.config(text="Осталось времени: " + str(self.remainingTime))

    def draw_timer(self):
        self.progressTimerCanvas.delete("timer_arc")
        x0, y0, x1, y1 = 25, 25, 75, 75
        start_angle = 360
        step = 360/self.MAX_TIME
        extent = self.remainingTime * step
        self.progressTimerCanvas.create_arc(x0, y0, x1, y1, start=start_angle, extent=extent, style=tk.ARC, outline='blue', width=5,
                               tags="timer_arc")
        self.progressTimerCanvas.itemconfig(self.timer_label, text=str(self.remainingTime))

    def play_timer(self):
        path = _defs_.getStandartPath() + "timer" + str(self.remainingTime) + _defs_.get_MP3()

        if not os.path.exists(path):
            _defs_.create_gtts("ru", str(self.remainingTime), path)

        if self.remainingTime == self.MAX_TIME / 2 and not os.path.exists(self.half_path):
            _defs_.create_gtts("ru", "Половина времени", self.half_path)

        if self.remainingTime == self.MAX_TIME - 1 and not os.path.exists(self.full_path):
            _defs_.create_gtts("ru", "Отсчёт пошел", self.full_path)

        if self.remainingTime == self.MAX_TIME - 1:
            _defs_.play_sound(self.full_path)
        elif self.remainingTime == self.MAX_TIME / 2:
            _defs_.play_sound(self.half_path)
        elif self.remainingTime in (0, 1, 2, 3):
            _defs_.play_sound(path)

        #playsound(_defs_.getStandartPath()+"timer"+_defs_.get_MP3())

    def play_camera_broken(self):
        path = _defs_.getStandartPath() + "camera_BR" + _defs_.get_MP3()

        if not os.path.exists(path):
            _defs_.create_gtts("ru",
                               "К сожалению Вас не видит ни одна камера! "
                               "Возможно, дело в драйверах системы. Обязательно перезапустите приложение!", path)
        _defs_.play_sound(path)


    def timer_function(self):
        if not self.isBroken:
            if self.remainingTime > 0:
                self.remainingTime -= 1
                #self.update_label()
                if (not self.yogaObject.getCommentsMode()
                        and self.remainingTime in (0, 1, 2, 3, self.MAX_TIME - 1, self.MAX_TIME / 2)):
                    self.play_timer()
                self.draw_timer()
                self.after(1000, self.timer_function)
            else:
                self.isExpired = True
                self.yogaObject.setTimeInTraining(self.MAX_TIME)
        else:
            self.play_camera_broken()


    def showVideoCamera(self):
        # make the cicle!
        ret1, frame1 = self.userCameraVideo.read()

        print(ret1, " + ", self.isExpired)
        # time's expired
        if ret1 and self.isExpired:
            # first - camera's release, next -> next exersize
            self.userCameraVideo.release()
            self.nextExersize()
            #print("Out1")
            return

        if not ret1:
            if not self.isExpired:
                print("not expired")
                self.cameraClass.try_to_find_another_camera()
                self.cameraID = self.cameraClass.returnSelectedCameraID()
                if (self.cameraID != -1):
                    self.findCamera()
                    #if hasattr(self, 'training_run'):  # Check if the function run
                    #    self.after_cancel(self.training_run)
                    self.showVideoCamera()
                else:
                    #print("Out2")
                    self.userCameraVideo.release()

                    img2 = Image.fromarray(frame2)
                    imgtk2 = ImageTk.PhotoImage(image=img2)
                    self.photoCanvas.imgtk = imgtk2
                    self.photoCanvas.create_image(0, 0, anchor=tk.NW, image=imgtk2)

                    nocamera = _defs_.getConvertedImage(_defs_.getStandartPath() + "camera" + _defs_.get_PNG(), self.canvasWidth, self.canvasHeight)

                    self.cameraCanvas.imgtk = nocamera
                    self.cameraCanvas.create_image(0, 0, anchor=tk.NW, image=nocamera)

                    if not self.isBroken:
                        self.update()
                        self.after(10, self.showVideoCamera)
                        self.isBroken = True
                    else:
                        logging.error("Camera lost during the training")
                        self.showErrorMessage("Вы вас не видим! Проверьте еще раз камеру!")

                    return

        if ret1:
            frame1 = cv2.flip(frame1, 1)
            frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
            frame1 = cv2.resize(frame1, (self.canvasWidth, self.canvasHeight))
            results1 = self.poses[0].process(frame1)

            if results1.pose_landmarks:
                self.mp_drawing.draw_landmarks(frame1, results1.pose_landmarks, self.mp_poses.POSE_CONNECTIONS)

            try:
                if results1.pose_landmarks and results2.pose_landmarks:
                    self.highlight_mismatch(frame1, frame2, results1.pose_landmarks.landmark,
                                       results2.pose_landmarks.landmark)
            except NameError:
                print("One of elements is not defined")

        #if ret1:
            #frame1 = cv2.resize(frame1, (self.canvasWidth, self.canvasHeight))

            img1 = Image.fromarray(frame1)
            imgtk1 = ImageTk.PhotoImage(image=img1)
            self.cameraCanvas.imgtk = imgtk1
            self.cameraCanvas.create_image(0, 0, anchor=tk.NW, image=imgtk1)

            img2 = Image.fromarray(frame2)
            imgtk2 = ImageTk.PhotoImage(image=img2)
            self.photoCanvas.imgtk = imgtk2
            self.photoCanvas.create_image(0, 0, anchor=tk.NW, image=imgtk2)

            self.update()
            self.training_run = self.after(10, self.showVideoCamera)


    def findCamera(self):
        self.cameraID = self.cameraClass.returnSelectedCameraID()
        self.userCameraVideo = cv2.VideoCapture(self.cameraID)
        self.isBroken = False

    def poseCamera(self):
        # camera catch

        #self.userCameraVideo = cv2.VideoCapture(self.cameraID)
        self.yogaPicture = cv2.imread(_defs_.getStandartPath() + self.yogaObject.getCurrentElementFromYoga() + _defs_.get_PNG())
        self.exercise_handler()

        #self.isBroken = False
        self.isExpired = False

        self.iterNumber = 0
        self.CURRENT_SCORE = 0

        self.timer_function()

        #self.successfuly_released = False
        #self.cameraID = self.cameraClass.returnSelectedCameraID()

        self.findCamera()
        self.showVideoCamera()


    def showErrorMessage(self, name):
        showerror("Ошибка", name)
        self.errorCameraButton.config(state=tk.NORMAL)


    def emergencyExit(self):
        self.errorCameraButton.config(state=tk.DISABLED)
        self.controller.show_frame("StartMenuSecond")


    def nextExersize(self):
        self.yogaObject.setNextElementFromYogaList()

        self.remainingTime = self.MAX_TIME

        #self.RESULTING_SCORE += int(( self.CURRENT_SCORE/self.iterNumber )/self.yogaObject.getYoursYogaListLen())
        try:
            self.RESULTING_SCORE += self.CURRENT_SCORE/self.iterNumber
        except ZeroDivisionError:
            print("Camera's broken!")
        #print(self.RESULTING_SCORE)

        if (self.yogaObject.getCurrentElementFromYoga() != "null"):
            self.controller.show_frame("TrainingWaiting")
        else:
            # open return-frame
            db = DataBaseInfo()
            db.set_DATETIME_END()
            self.yogaObject.setUsersRecord(self.RESULTING_SCORE/self.yogaObject.getYoursYogaListLen())
            self.controller.show_frame("ResultTraining")


