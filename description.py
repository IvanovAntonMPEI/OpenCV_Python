# -*- coding: utf-8 -*-
import os, cv2
from Helper import *

class Description(Helper):

    black_name = '.DS_Store'
    format_file = '.dat'

    def create_str(self, folder, name, list_str, counter, divine = ' '):
        string = os.path.join(folder, name) + divine

        for i in list_str:
            string += str(i) + divine
        return string[:-1]

    # создает строку описания картинки
    def create_file_str(self, img):
        size = self.create_size(img)
        return [1, 0, 0, size[0], size[1]]

    def create_list_file(self, name_folder):
        list_dir = os.listdir(name_folder)
        return [i for i in list_dir if not (self.black_name in i)]

    def create_description_file(self, name_file, name_folder):

        # name_file - название итогового файла
        # name_folder - папка с изображениями

        print(name_file, name_folder)

        # создание файла описания
        name_folder = self.change_path(name_folder)

        ret_str = ''

        list_dir = self.create_list_file(name_folder)

        for number, i in enumerate(list_dir):
            img = cv2.imread(os.path.join(name_folder, i))

            if (not img is None):
                desc = self.create_file_str(img)
                ret_str += self.create_str(name_folder, i, desc, number) + "\n"

        fl = open(name_file, 'w')
        fl.write(ret_str[:-1])
        fl.close()


    def create_bad_file(self, name_file, name_folder):
        # name_file - имя итогового файла
        # name_folder - папка с Bad изображениями

        name_folder = self.change_path(name_folder)

        list_dir = self.create_list_file(name_folder)

        ret_str = ''

        for i in list_dir:
            ret_str += os.path.join(name_folder, i) + '\n'

        fl = open(name_file, 'w')
        fl.write(ret_str[:-1])
        fl.close()
