import locale

from tkinter import filedialog
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt


# face_path ='face.png'
class Feature_Matching:
    def __init__(self, window, selected_file_date):
        locale.setlocale(locale.LC_ALL, 'de_DE')  # use German locale; name might vary with platform
        self.top = window
        self.selected_file_date = selected_file_date
        self.face_path = filedialog.askopenfilename(parent=self.top,initialdir=".", title="Select the face photo"
                                                       , filetypes=(
                ("png files", "*.png"), ("jpg files", "*.jpg"), ("all files", "*.*")))

        # self.selected_file_date = '2021_02_08_T_20_54_25__812.png'
        self.selected_file_date = selected_file_date
        self.img1 = cv.imread(self.face_path,cv.IMREAD_GRAYSCALE)          # queryImage
        self.img2 = cv.imread(self.selected_file_date,cv.IMREAD_GRAYSCALE) # trainImage
        # Initiate SIFT detector
        sift = cv.SIFT_create()
        # find the keypoints and descriptors with SIFT
        kp1, des1 = sift.detectAndCompute(self.img1,None)
        kp2, des2 = sift.detectAndCompute(self.img2,None)
        # FLANN parameters
        FLANN_INDEX_KDTREE = 1
        index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
        search_params = dict(checks=50)   # or pass empty dictionary
        flann = cv.FlannBasedMatcher(index_params,search_params)
        matches = flann.knnMatch(des1,des2,k=2)
        # Need to draw only good matches, so create a mask
        matchesMask = [[0,0] for i in range(len(matches))]
        # ratio test as per Lowe's paper
        for i,(m,n) in enumerate(matches):
            if m.distance < 0.7*n.distance:
                matchesMask[i]=[1,0]
        draw_params = dict(matchColor = (0,255,0),
                           singlePointColor = (255,0,0),
                           matchesMask = matchesMask,
                           flags = cv.DrawMatchesFlags_DEFAULT)
        self.list_kp1 = []
        self.list_kp2 = []

        # For each match...
        for mat in matches:

            # Get the matching keypoints for each of the images
            img1_idx = mat[0].queryIdx
            img2_idx = mat[0].trainIdx

            # x - columns
            # y - rows
            # Get the coordinates
            (x1, y1) = kp1[img1_idx].pt
            (x2, y2) = kp2[img2_idx].pt

            # Append to each list
            self.list_kp1.append((int(x1), int(y1)))
            self.list_kp2.append((int(x2), int(y2)))

        # print(type(list_kp2.index(1)))
        # print(min(self.list_kp2))
        min_point =min(self.list_kp2)
        max_point = max(self.list_kp2)

        print(self.list_kp2)
        print(self.list_kp1)

        img3 = cv.drawMatchesKnn(self.img1,kp1,self.img2,kp2,matches,None,**draw_params)
        img4 = cv.cvtColor(cv.imread(self.selected_file_date), cv.COLOR_BGR2RGB)
        # cv.rectangle(img4,max_point,min_point,(0,255,0),1)
        # img4 = cv.rectangle(self.img1,(10,10),(30,30),(0,255,0),10)
        height, width = self.img1.shape[:2]

        for i in self.list_kp2:
            cv.circle(img4,i,3,(0,255,0),1)

        plt.imshow(img4)


        plt.subplot(1,2,1)
        plt.imshow(img4)
        plt.title('Matching Keypoints')

        plt.subplot(1,2,2)
        plt.imshow(img3)
        plt.title('DrawMatchesKnn')

        plt.show()

