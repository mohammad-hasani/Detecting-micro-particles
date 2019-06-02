import cv2


def get_maximum_pixel_in_image(img):
    maximum = 0
    for i in img:
        for j in i:
            if j > maximum:
                maximum = j
    return maximum


def get_average_pixel_in_image(img):
    sum = 0
    for i in img:
        for j in i:
            sum += j
    denominator = img.shape[0] * img.shape[1]
    average = int(sum / denominator)
    return average


def get_details(img, dictionary):
    labels = list()
    values = list()
    for i in dictionary.keys():
        d = dictionary[i]
        img_tmp = img.copy()

        labels.append(int(d[0][4]))
        values.append(len(d))

        for j in d:
            counter = j[0]
            x, y = j[1]
            w, h = j[2]
            avg = j[4]

            img_tmp = cv2.rectangle(img_tmp, (x, y), (x + w, y + h), (0, 255, 0), 1)

            # add number
            font = cv2.FONT_HERSHEY_SIMPLEX
            position = (x, y)
            fontScale = .3
            fontColor = (255, 255, 255)
            lineType = 1

            img_tmp = cv2.putText(img_tmp, str(counter),
                        position,
                        font,
                        fontScale,
                        fontColor,
                        lineType)
            with open('details.xls', 'a') as f:
                f.write(str(counter) + ', ' + str(avg))
                f.write('\n')
        img_name = int(d[0][4])
        cv2.imwrite('details' + str(img_name) + '.jpg', img_tmp)

