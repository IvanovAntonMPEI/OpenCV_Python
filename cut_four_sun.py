# -*- coding: utf-8 -*-

import cv2
import numpy as np
from PIL import Image
import time, os
import sys, subprocess
from Helper import *


from threading import Thread

path_cascad = '/home/adminivanov/Рабочий стол/Open_CV/V77/haarcascade/cascade.xml'
cascade = cv2.CascadeClassifier(path_cascad)


class Plot_Image():

    img = None

    flag_thread = False

    max_code = 10

    cap = None

    def __init__(self, code = None, time_sleep = 1e-3):

        self.initialize(code)
        self.time_sleep = time_sleep

    def __del__(self):
        if (self.cap):
            self.clearCapture(self.cap)

    def initialize(self, code):
        if not code is None:
            self.cap = cv2.VideoCapture(code)

    def set_image(self, img):
        if (not img is None):
            self.img = img

    def get_image(self):
        return self.img

    def step(self):
        if self.cap:
            ret, img = self.cap.read()
            self.set_image(img)

    def show_image(self):
        if not cv2.waitKey(10) == 27: # Клавиша Esc
            cv2.imshow("camera", self.get_image())
            #pass

    def thread_plot(self):
        self.update_thread()

        while(self.flag_thread):
            self.step()
            self.show_image()
            time.sleep(self.time_sleep)

    def stop(self):
        self.flag_thread = False

    def update_thread(self):
        self.flag_thread = True

    def clearCapture(self, capture):
        capture.release()
        cv2.destroyAllWindows()

    def get_code(self):
        ret_list = []

        for i in range(self.max_code):

            try:
                cap = cv2.VideoCapture(i)
                ret, frame = cap.read()
                cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                ret_list.append(i)

            except:
                pass

            self.clearCapture(cap)

        return ret_list

class Handler_Point(Helper):

    path_folder = "Image"
    name_image = "image"
    format_image = '.png'

    scale_w = 0.85
    scale_h = 0.85

    # принимаем объекты Point
    def __init__(self, list_object, path_folder = None, name_image = None, time_work = 10, flag_time = False, counter_image = 5):
        self.list_object = list_object
        self.create_dir()
        self.init()
        self.time_work = time_work
        self.flag_time = flag_time
        self.flag_image = not flag_time

        self.number_image = counter_image
        self.counter_save_image = 0

    def run(self):
        self.time_start = time.time()

    def init(self):
        self.counter_image = 0

    def check_init(self):
        flag = [i.get_init() for i in self.list_object]
        return not(False in flag)

    def plot_object(self, img):
        if(self.check_init()):
            coord_list = [i.ret_coord_list for i in self.list_object]
            point = self.get_point(coord_list)
            img = cv2.rectangle(img, (point[0][0], point[1][0]),(point[0][1], point[1][1]), (0, 0, 255), 2)
        return img

    def tick(self, img):
        #  создает новую картинку вырезанную
        if(self.check_init()):
            coord_list = [i.ret_coord_list for i in self.list_object]
            new_img = self.cut_img(coord_list, img)
            self.save_image(new_img)

    def check_end(self):
        if (self.flag_time):
            flag_end = (time.time() - self.time_start > self.time_work)
        else:
            flag_end = (self.counter_image % self.number_image) == 0 and self.counter_image > 0

        if (flag_end):
            self.init()
            [i.clear() for i in self.list_object]

        return flag_end

    def get_point(self, coord_list):
        distance = lambda x, y: (x**2 + y**2)**0.5

        distance_list = [distance(i[0], i[1]) for i in coord_list]

        list_x = [i[0] for i in coord_list]
        list_y = [i[1] for i in coord_list]

        index_w_min = list_x.index(min(list_x))
        index_h_min = list_y.index(min(list_y))

        ret = [(list_x[index_w_min] + coord_list[index_w_min][2], max(list_x)), (list_y[index_h_min] + coord_list[index_h_min][3], max(list_y))]
        ret = [list(map(int, i)) for i in ret]

        #index_min = distance_list.index(min(distance_list))
        #index_max = distance_list.index(max(distance_list))

        #ret = [(coord_list[index_min][0] + coord_list[index_min][2] * self.scale_w, coord_list[index_max][0] * 1.03), (coord_list[index_min][1] + coord_list[index_min][3] * self.scale_h, coord_list[index_max][1] * 1.1)]
        #ret = [list(map(int, i)) for i in ret]

        return ret

    def cut_img(self, coord_list, img):
        point = self.get_point(coord_list)
        new_img = img[point[1][0]:point[1][1], point[0][0]:point[0][1]]
        #img[point_list[0][0] : point_list[1][0], point_list[0][1] : point_list[1][1]]
        return new_img

    def create_dir(self):
        subprocess.call('rm -rf ' + self.change_str_to_shell(self.path_folder), shell = True)
        subprocess.call('mkdir ' + self.change_str_to_shell(self.path_folder), shell = True)

    def create_path(self):
        name =  self.name_image + str(self.counter_save_image) + self.format_image
        return os.path.join(self.path_folder, name)

    def save_image(self, img):
        cv2.imwrite(self.create_path(), img)
        self.counter_image += 1
        self.counter_save_image += 1
        #print(self.create_path(), self.counter_image)

    def check_detected(self):
        if (self.check_init()):
            flag = [i.check_detected() for i in self.list_object]

            if False in flag:
                [i.clear() for i in self.list_object]


class Point:
# класс описывающий одну метку
    coord_list = []
    ret_coord_list = []

    list_object = []

# Объект инициализирован
    flag_init = False

# Объект находится в подозрении на добавление
    flag_add = False
    flag_add_now = False

# Объект находится в подозрении на удаление
    flag_delete = False
    flag_delete_now = False

    max_error = 100

# шаг смещения
    step_bias = 0.8# !

# максимальный размер рамки
    max_size = 70

# счетчик для удаления
    counter_delete = 5 #  !

# счетчик добавления
    counter_add = 5 # !

    now_counter_delete = 0
    now_counter_add = 0

# уставка
    error_now = 0.5 * max_size # !

    counter_info = 0

# счетчики для обнаружение объекта
    counter_detected = 0
    counter_detected_last = 0

    def __init__(self, id):
        self.id = id

        self.create_list = lambda x: [(x[i] + x[i + 2])/2 for i in range(2)]
        self.error = lambda x, y: np.mean([abs(i - j) for (i,j) in zip(self.create_list(x), self.create_list(y))])

        self.clear()

    def full_update(self):
        self.init_add()
        self.init_delete()
        self.update_coord_list()
        self.flag_init = False

    def check_coord(self, coord):
        # проверяет параметры h и w
        return (coord[2] < self.max_size or coord[3] < self.max_size)

    def init_list(self, list_object):
        # лист из других объектов
        self.list_object = [i for i in list_object if not i is self]

    def init_delete(self):
        self.now_counter_delete = 0
        self.flag_delete_now = False
        self.flag_delete = False

    def get_init(self):
        return self.flag_init

    def init_add(self):
        self.now_counter_add = 0
        self.flag_add_now = False
        self.flag_add = False

    def change_coord(self, coord):
        return [[x, y, w, h] for (x, y, w, h) in coord]

    def tick(self, coord):
        coord = self.change_coord(coord)

        for i in coord:
            flag_add = False
            flag_delete = False

            if (self.check_point(i) and self.check_coord(i)):

                flag_error = self.flag_error(self.get_error(i))

                if (not self.flag_init and not self.flag_add):
                    # на текущий момент нету инициализованной метки и у других
                    # объектов данная метка не инициализована
                    self.coord_list = i
                    self.init_add()
                    self.flag_add = True

                elif (self.flag_add):
                    # проверяем а та ли эта точка, которая сейчас находится
                    # под подозрением на добавление
                    if (not flag_error):
                        flag_add = True

                elif (self.flag_init):
                    # метка инициализирована
                    if (not flag_error):
                        flag_delete = True
                        self.bias_coord_list(i)

                self.flag_add_now = self.flag_add_now or flag_add
                self.flag_delete_now = self.flag_delete_now or flag_delete

        self.now_counter_delete += 1
        self.now_counter_add += 1

        self.analyz_add()
        self.analyz_delete()
        #self.info()

    def plot_object(self, img):
        if self.flag_init:
            img = cv2.rectangle(img, (self.ret_coord_list[0], self.ret_coord_list[1]),
            (self.ret_coord_list[0] + self.ret_coord_list[2], self.ret_coord_list[1] + self.ret_coord_list[3]), (255, 0, 0), 2)
        return img

    def info(self):
        self.counter_info += 1

        if (self.counter_info%10 == 0 and self.counter_info > 0):
            print("\n=======================")
            print("I object " + str(self.id) + "\n" + "flag_init: " + str(self.flag_init))
            print("Flag_add: " + str(self.flag_add) + " " + str(self.flag_add_now))
            print("Coord ")
            print("Counter: " + str(self.now_counter_add) + " " + str(self.now_counter_delete))
            print(self.ret_coord_list)
            print("=======================\n")

            #self.counter_info = 0


    def check_point(self, coord):
        # проверка принадлежности данной точки к другим объектам
        ret = True

        for i in self.list_object:
            error = self.error(i.get_coord(), coord)
            #print("Error:" + str(error))

            if (not self.flag_error(error)):
                ret = False
                break

        return ret

    def analyz_add(self):
        if (self.flag_add and self.now_counter_add >= self.counter_add):
            #print("ADD " + str(self.id) + " " + str(self.flag_add_now))

            # прошло несколько тактов => анализируем
            if (self.flag_add_now):
                #print("YEAP!", self.coord_list)
                # был замечен хотя бы 1 раз такой объект => добавляем
                self.ret_coord_list = self.coord_list
                self.flag_init = True
                self.init_delete()
            else:
                # очищаем список и обнуляем счетчик
                self.update_coord_list()

            self.init_add()

    def clear(self):
        #  удаление текущих координат
        self.update_coord_list()
        self.full_update()

    def update_counter_detected(self):
        self.counter_detected += 1

    def check_detected(self):
        flag = True
        if (self.get_init()):
            flag = self.counter_detected != self.counter_detected_last
            self.counter_detected_last = self.counter_detected
        return flag

    def analyz_delete(self):
        if (self.flag_init and self.now_counter_delete >= self.counter_delete):
            # прошло несколько тактов => анализируем
            #print("DELETE " + str(self.id) + " " + str(self.flag_delete_now))
            if (not self.flag_delete_now):
                # очищаем список и обнуляем счетчик
                self.clear()

            # иначе
            # был замечен хотя бы 1 раз такой объект => оставляем

            self.init_delete()

    def get_coord(self):
        return self.coord_list

    def get_error(self, coord_list):
        return self.error(self.coord_list, coord_list)

    def flag_error(self, error):
        # ошибка больше допустимой ?
        return error > self.error_now

    def bias_coord_list(self, coord):
        if (self.flag_init):
            self.ret_coord_list = [int((1 - self.step_bias)*i + self.step_bias * j) for (i, j) in zip(self.ret_coord_list, coord)]

    def update_coord_list(self):
         self.coord_list = [0] * 4
         self.ret_coord_list = [0] * 4
