import locale

import cv2



class Select_mask():
    def __init__(self, selected_file_date, thermal_image_size, int_raduis, shape_value, width=0, height=0):
        locale.setlocale(locale.LC_ALL, 'de_DE')  # use German locale; name might vary with platform
        self.drawing = False
        self.width = width
        self.height = height
        self.shape_value = shape_value
        self.thermal_image_size = thermal_image_size
        self.selected_file_date = selected_file_date
        self.my_photo = cv2.cvtColor(cv2.imread(self.selected_file_date), cv2.COLOR_BGR2RGB)
        self.int_raduis = int_raduis
        # pts = np.array([[0, 5], [1, 4], [10, 20], [50, 10]], np.int32)
        # pts = pts.reshape((-1, 1, 2))
        # my_photo = cv2.polylines(my_photo, [pts], True, (0, 255, 255))
        # cv2.imshow("Select the mask", my_photo)
        # cv2.namedWindow('Select the mask')
        cv2.namedWindow('image')

        self.res = cv2.resize(self.my_photo, self.thermal_image_size)
        cv2.setMouseCallback("image", self.draw_circle)




    # mouse callback function
    def draw_circle(self, event, x, y, flags, param):
        # explain types of event!
        # if event == cv2.EVENT_LBUTTONUP:
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawing = True
        elif event == cv2.EVENT_MOUSEMOVE:
            if self.drawing == True:

                # cv2.circle(my_photo, (10, 10), int_raduis, (0, 255, 0), -1)
                print(self.shape_value)
                if self.shape_value ==0:
                    cv2.circle(self.res, (x, y), self.int_raduis, (0, 255, 0), -1)
                elif self.shape_value ==1:
                    # cv2.rectangle(self.res,x,y,1,(0, 255, 0), -1)
                    cv2.rectangle(self.res, (x-(self.width//2), y-(self.height//2)), (x+(self.width//2), y+(self.height//2)), (0, 255, 0), -1)
        elif event == cv2.EVENT_LBUTTONUP:
            self.drawing = False
    def start(self):
        while (1):
            cv2.imshow('image', self.res)
            if cv2.waitKey(20) & 0xFF == 27:
                cv2.destroyAllWindows()
                return
        cv2.destroyAllWindows()


