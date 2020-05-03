# -*- coding: utf-8 -*-

import cv2
from description import *
from cut_four_sun import *

def run(code = 2, counter_plot = 3):

    Image_Show = Plot_Image(code)
 # Read image with opencv
    #Image_Show.thread_plot()

    list_object = [Point(i) for i in range(4)]
    [i.init_list(list_object) for i in list_object]

    print_counter = 50
    check_counter = 1
    counter = 0

    handler = Handler_Point(list_object, flag_time = False)
    handler.run()

    Image_Show.step()

    str_list = ["Выставьте камеру прямо",
    #"Выставьте камеру слева",
    #"Выставьте камеру справа",
    #"Выставьте камеру сверху",
    #"Выставьте камеру снизу",
    ]

    for k in str_list:

        try:
            thread = Thread(target = Image_Show.thread_plot, args = ())
            Image_Show.update_thread()
            thread.start()
            input(k)

            Image_Show.stop()
            thread.join()

            #Image_Show.stop()
            #thread.join()
        except:
            pass

        print("check", not handler.check_end())
        while not handler.check_end():
            #print("asd")
            img = Image_Show.get_image()

            if(counter % check_counter == 0 and counter > 0) or True:
                coord = Helper().detect_sun(img, cascade)

                [i.tick(coord) for i in list_object]
                counter = 0

                img = handler.plot_object(img)
                #handler.check_detected()
                #handler.tick(img)

                for i in list_object:
                    img = i.plot_object(img)

                for (x, y, w, h) in coord:
                    img = cv2.rectangle(img, (x, y), ((x + w), (y + h)), (0, 255, 0), 2)

            Image_Show.set_image(img)
            Image_Show.show_image()
            Image_Show.step()

            #cv2.imshow("camera", img)
            counter += 1
            time.sleep(5e-3)



    desc = Description()
    desc.create_description_file("Good_desc.dat", Handler_Point.path_folder)


    Image_Show.__del__()
    cv2.destroyAllWindows()

    print ("------ Done -------")

Image_Show = Plot_Image()
number = Image_Show.get_code()
#print("Number: ", number)
run(max(number))
