import cv2
import tools
import random
import matplotlib.pyplot as plt
from decimal import Decimal, ROUND_DOWN
import numpy as np


def plot_bar(labels, values, name):
    plt.bar(labels, values)
    plt.xlabel('size', fontsize=5)
    plt.ylabel('distribution', fontsize=5)
    # plt.xticks(index, label, fontsize=5, rotation=30)
    plt.title('Micro')
    plt.savefig('bar_plot' + str(name) + '.jpg')
    plt.clf()


# test1 200um 63
# test2 20um
# test3-1 200um 63
# test3-2 20um
# test4 50um 90

# 21.5 * 20 um , t  63
def main():
    path = './test4/test4.jpg'
    measurement = 21.5 * 20 / 768

    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh1 = cv2.threshold(gray, 90, 255, cv2.THRESH_BINARY)
    # thresh1 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 101, 2)
    # kernel = np.ones((5, 5), np.uint8)
    # thresh1 = cv2.morphologyEx(thresh1, cv2.MORPH_OPEN, kernel)
    # thresh1 = cv2.morphologyEx(thresh1, cv2.MORPH_CLOSE, kernel)


    # find Contours
    im2, contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(img, contours, -1, (0, 255, 0), 1)

    counter = 0
    dictionary = dict()
    for i, v in enumerate(contours):

        # if random.random() > .3:
        #     continue

        if hierarchy[0][i][3] != -1:
            continue

        x, y, w, h = cv2.boundingRect(v)

        width = w * measurement
        height = h * measurement
        avg = (width + height) / 2
        avg_int = int(avg)

        if avg_int in dictionary:
            l = list()
            l.append(counter)
            l.append((x, y))
            l.append((w, h))
            l.append((width, height))
            l.append(avg)
            dictionary[avg_int].append(l)
        else:
            l = list()
            l.append(counter)
            l.append((x, y))
            l.append((w, h))
            l.append((width, height))
            l.append(avg)
            dictionary[avg_int] = list()
            dictionary[avg_int].append(l)
        counter += 1

    labels = list()
    values = list()
    labels.append(list())
    values.append(list())
    k = 1
    for i in dictionary.keys():
        d = dictionary[i]

        count = len(d)
        if count > 100:
            labels.append(list())
            values.append(list())
            d_temp = dict()
            for j in d:
                avg = j[4]
                rounded = Decimal(avg).quantize(Decimal('.1'), rounding=ROUND_DOWN)
                rounded = float(rounded)
                if rounded in d_temp:
                    d_temp[rounded].append(avg)
                else:
                    d_temp[rounded] = list()
                    d_temp[rounded].append(avg)
            for j in d_temp.keys():
                labels[k].append(str(j))
                values[k].append(len(d_temp[j]))
            print(labels[k])
            print(values[k])
            plot_bar(labels[k], values[k], str(k))
            k += 1

        else:
            labels[0].append(int(d[0][4]))
            values[0].append(len(d))


    plot_bar(labels[0], values[0], 'main')
    tools.get_details(img, dictionary)

    # cv2.imshow('s', thresh1)
    #
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # cv2.imwrite('/home/sina/Desktop/details.jpeg', img)


if __name__ == '__main__':
    main()