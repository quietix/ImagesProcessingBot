import json
import os
from pprint import pprint
from PIL import Image
import telepot

token = '5099222715:AAFChikYgr5R3m0ezz9H0jhHVnKdInvrtGo'
bot = telepot.Bot(token)

commands = ['/start', '/help', '/inversion', '/blure', '/clarity', '/median', '/sobel', '/2bit', '/watersign']


# invertion, blure, sobel, clarity, medial (is not in real commands in tg because of error in working)
# *******************************************************************************************************


class Photo_service_class:

    @staticmethod
    def invertion(photo_path, request_body):
        array = request_body['message']['photo']
        len1 = len(array)
        file_id = request_body['message']['photo'][len1 - 1]['file_id']
        image = Image.open(f'{photo_path}').convert('RGB')
        width, height = image.size
        for i in range(width):
            for j in range(height):
                (red, green, blue) = image.getpixel((i, j))
                new_red = 255 - red
                new_green = 255 - green
                new_blue = 255 - blue
                (new_red, new_green, new_blue) = checkPixelBorders(new_red, new_green, new_blue)
                image.load()
                image.putpixel((i, j), (new_red, new_green, new_blue))

        new_photo_path = f'{file_id}.png'
        image.save(f'{new_photo_path}')
        return new_photo_path

    @staticmethod
    def median(photo_path, request_body):
        array = request_body['message']['photo']
        len1 = len(array)
        file_id = request_body['message']['photo'][len1 - 1]['file_id']
        inputImage = Image.open(f'{photo_path}').convert('RGB')
        width, height = inputImage.size
        len_of_matrix = 3
        matrixR = matrixG = matrixB = create_2d_array(len_of_matrix, len_of_matrix)
        for k in range(width):
            for l in range(height):
                resR = resG = resB = 0
                for i in range(len_of_matrix):
                    for j in range(len_of_matrix):
                        (x, y) = set_X_Y(k, l, i, j, width, height)
                        (red, green, blue) = inputImage.getpixel((x, y))
                        matrixR[i][j] = red
                        matrixG[i][j] = green
                        matrixB[i][j] = blue
                arrayR = transform_2d_into_1d(matrixR)
                arrayG = transform_2d_into_1d(matrixG)
                arrayB = transform_2d_into_1d(matrixB)
                my_sort_array(arrayR)
                my_sort_array(arrayG)
                my_sort_array(arrayB)
                resR = arrayR[4]
                resG = arrayG[4]
                resB = arrayB[4]
                (resR, resG, resB) = checkPixelBorders(resR, resG, resB)
                inputImage.putpixel((k, l), (resR, resG, resB))
        new_photo_path = f'{file_id}.png'
        inputImage.save(f'{new_photo_path}')
        return new_photo_path


    @staticmethod
    def sobel(photo_path, request_body):
        array = request_body['message']['photo']
        len1 = len(array)
        file_id = request_body['message']['photo'][len1 - 1]['file_id']
        inputImage = Image.open(f'{photo_path}').convert('RGB')
        width, height = inputImage.size
        specific_matrix = [
            [-1, -1, -1],
            [-1, 8, -1],
            [-1, -1, -1]
        ]
        len_of_matrix = 3
        for k in range(width):
            for l in range(height):
                resR = resG = resB = 0
                for i in range(len_of_matrix):
                    for j in range(len_of_matrix):
                        (x, y) = set_X_Y(k, l, i, j, width, height)
                        (red, green, blue) = inputImage.getpixel((x, y))
                        resR += red * specific_matrix[j][i]
                        resG += green * specific_matrix[j][i]
                        resB += blue * specific_matrix[j][i]
                (resR, resG, resB) = checkPixelBorders(resR, resG, resB)
                inputImage.putpixel((k, l), (resR, resG, resB))
        new_photo_path = f'{file_id}.png'
        inputImage.save(f'{new_photo_path}')
        return new_photo_path

    @staticmethod
    def clarity(photo_path, request_body):
        array = request_body['message']['photo']
        len1 = len(array)
        file_id = request_body['message']['photo'][len1 - 1]['file_id']
        inputImage = Image.open(f'{photo_path}').convert('RGB')
        width, height = inputImage.size
        specific_matrix = [
            [-1, -1, -1],
            [-1, 9, -1],
            [-1, -1, -1]
        ]
        len_of_matrix = 3
        for k in range(width):
            for l in range(height):
                resR = resG = resB = 0
                for i in range(len_of_matrix):
                    for j in range(len_of_matrix):
                        (x, y) = set_X_Y(k, l, i, j, width, height)
                        (red, green, blue) = inputImage.getpixel((x, y))
                        resR += int((red * specific_matrix[j][i]))
                        resG += int((green * specific_matrix[j][i]))
                        resB += int((blue * specific_matrix[j][i]))
                (resR, resG, resB) = checkPixelBorders(resR, resG, resB)
                inputImage.putpixel((k, l), (resR, resG, resB))
        new_photo_path = f'{file_id}.png'
        inputImage.save(f'{new_photo_path}')
        return new_photo_path


    @staticmethod
    def blure(photo_path, request_body):
        array = request_body['message']['photo']
        len1 = len(array)
        file_id = request_body['message']['photo'][len1 - 1]['file_id']
        inputImage = Image.open(f'{photo_path}').convert('RGB')
        width, height = inputImage.size
        specific_matrix = [
            [1, 2, 1],
            [2, 4, 2],
            [1, 2, 1]
        ]
        len_of_matrix = 3
        for k in range(width):
            for l in range(height):
                resR = resG = resB = 0
                for i in range(len_of_matrix):
                    for j in range(len_of_matrix):
                        (x, y) = set_X_Y(k, l, i, j, width, height)
                        (red, green, blue) = inputImage.getpixel((x, y))
                        resR += int((red * specific_matrix[j][i]) / 16)
                        resG += int((green * specific_matrix[j][i]) / 16)
                        resB += int((blue * specific_matrix[j][i]) / 16)
                (resR, resG, resB) = checkPixelBorders(resR, resG, resB)
                inputImage.putpixel((k, l), (resR, resG, resB))
        new_photo_path = f'{file_id}.png'
        inputImage.save(f'{new_photo_path}')
        return new_photo_path


def set_X_Y(k, l, i, j, width, height):
    x = k + i
    y = l + j
    if x > width - 1:
        x = width - 1
    if y > height - 1:
        y = height - 1
    return x, y


# *******************************************************************************************************


class Commands_service_class:
    @staticmethod
    def is_command(command):
        if command in commands:
            return True
        else:
            return False

    def find_user_last_command(self, data, request_body):
        chat_id = request_body['message']['chat']['id']
        username = request_body['message']['from']['username']
        data.reverse()
        index = 0
        for i in range(len(data)):
            if username == data[i]['message']['from']['username'] and self.is_command(data[i]['message']['text']):
                return data[i]['message']['text']
        sendMessage(chat_id, "Error")

    @staticmethod
    def execute_last_command(last_command, request_body):
        photo_path = downloadImage(request_body)
        if last_command == commands[2]:
            new_photo_path = Photo_service_class.invertion(photo_path, request_body)
            send_photo(request_body, new_photo_path)
        if last_command == commands[3]:
            new_photo_path = Photo_service_class.blure(photo_path, request_body)
            send_photo(request_body, new_photo_path)
        if last_command == commands[6]:
            new_photo_path = Photo_service_class.sobel(photo_path, request_body)
            send_photo(request_body, new_photo_path)
        if last_command == commands[4]:
            new_photo_path = Photo_service_class.clarity(photo_path, request_body)
            send_photo(request_body, new_photo_path)


    def clean_data_file(self):
        with open('data.json', 'r') as rd:
            data_list: list = json.load(rd)
            if len(data_list) > 150:
                del data_list[:10]

        with open('data.json', 'w') as fp:
            json.dump(data_list, fp, indent=4)


    def commands_service_def(self, request_body):
        chat_id = request_body['message']['chat']['id']
        data_list = list()

        if 'text' in request_body['message']:
            # self.clean_data_file()     TODO
            text = request_body['message']['text']
            command = text.split()
            if command[0] == commands[0] or command[0] == commands[1]:
                start(chat_id)
            elif self.is_command(command[0]):
                with open('data.json', 'r') as rd:
                    data_list = json.load(rd)
                data_elem = {
                    "update_id": request_body['update_id'],
                    "message": {
                        "message_id": request_body['message']['message_id'],
                        "from": {
                            "id": request_body['message']['from']['id'],
                            "is_bot": request_body['message']['from']['is_bot'],
                            "first_name": request_body['message']['from']['first_name'],
                            "username": request_body['message']['from']['username'],
                            "language_code": request_body['message']['from']['language_code']
                        },
                        "chat": {
                            "id": request_body['message']['chat']['id'],
                            "first_name": request_body['message']['chat']['first_name'],
                            "username": request_body['message']['chat']['username']
                        },
                        "date": request_body['message']['date'],
                        "text": request_body['message']['text'],
                        "type": request_body['message']['entities'][0]['type']
                    }
                }
                data_list.append(data_elem)
                with open('data.json', 'w') as fp:
                    json.dump(data_list, fp, indent=4)

        elif 'photo' in request_body['message']:
            with open('data.json', 'r') as rd:
                loaded_file = json.load(rd)
            last_command = self.find_user_last_command(loaded_file, request_body)
            sending_message_text = f'Executing {last_command}'
            sendMessage(chat_id, sending_message_text)
            self.execute_last_command(last_command, request_body)
        else:
            sendMessage(chat_id, "You sent me some дічь")


# *******************************************************************************************************


def start(chat_id):
    # sendMessage(chat_id, "Firstly send image, then choose process")
    sendMessage(chat_id, "Firstly choose process, then send image")


def getTelegramFilePath(file_id):
    tgFilePath = bot.getFile(file_id)
    return tgFilePath


def checkPixelBorders(r, g, b):
    if r > 255:
        r = 255
    elif r < 0:
        r = 0
    if g > 255:
        g = 255
    elif g < 0:
        g = 0
    if b > 255:
        b = 255
    elif b < 0:
        b = 0
    return r, g, b


def send_photo(request_body, path):
    chat_id = request_body['message']['chat']['id']
    array = request_body['message']['photo']
    len1 = len(array)
    file_id = request_body['message']['photo'][len1 - 1]['file_id']
    bot.sendPhoto(chat_id, photo=open(f'{path}', 'rb'))
    os.remove(path)


def downloadImage(request_body):
    array = request_body['message']['photo']
    len1 = len(array)
    file_id = request_body['message']['photo'][len1 - 1]['file_id']
    path = f'{file_id}.png'
    bot.download_file(file_id, f'{path}')
    return path


def sendMessage(chat, mess):
    bot.sendMessage(chat, mess)


def create_2d_array(m, n):
    arr = []
    for i in range(m):
        interanal_arr = []
        for j in range(n):
            interanal_arr.append(0)
        arr.append(interanal_arr)
    return arr


def transform_2d_into_1d(arr_2d):
    res_arr = []
    raws = len(arr_2d)
    cols = len(arr_2d[0])
    for i in range(raws):
        for j in range(cols):
            res_arr.append(arr_2d[i][j])
    return res_arr


def my_sort_array(arr):
    for i in range(1, len(arr)):
        for j in range(1, len(arr)):
            if arr[j - 1] > arr[j]:
                tmp = arr[j - 1]
                arr[j - 1] = arr[j]
                arr[j] = tmp

    return arr