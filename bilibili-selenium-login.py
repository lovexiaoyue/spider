import re
import time
import random
import requests

from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains


class Bilibili(object):
    """selenium自动登陆bilibili"""

    def __init__(self, name, password):
        """初始化"""
        self.url = 'https://passport.bilibili.com/login'
        self.name = name
        self.password = password
        self.browser = webdriver.Chrome()

    def open_web_page(self):
        """打开网页"""
        self.browser.get(self.url)

    def push_name_password(self):
        """输入用户名密码"""
        # 输入用户名
        for i in self.name:
            self.browser.find_element_by_xpath('//*[@id="login-username"]').send_keys(i)
            time.sleep(0.1)

        # 输入密码
        for i in self.password:
            self.browser.find_element_by_xpath('//*[@id="login-passwd"]').send_keys(i)
            time.sleep(0.1)
        print('账号密码输入完成')

    def get_image(self):
        """获取验证码图片"""
        # 完整图片
        try:
            divs_full = self.browser.find_elements_by_xpath('//div[@class="gt_cut_fullbg_slice"]')

            # 获取图片url
            div = divs_full[0].get_attribute('style')
        except:
            return None, None
        # 将后缀替换为jpg
        url = re.findall('url\(\"(.*)\"\);', div)[0].replace('webp', 'jpg')
        # 将图片保存到本地
        response = requests.get(url)
        with open('full_image.jpg', 'wb') as f:
            f.write(response.content)
        print('完整图片下载完成')

        full_image_location_list = []
        # 获取位置信息
        for div in divs_full:
            location = {}
            data = div.get_attribute('style')
            location['x'] = int(re.findall('background-position: (.*)px (.*)px;', data)[0][0])
            location['y'] = int(re.findall('background-position: (.*)px (.*)px;', data)[0][1])
            full_image_location_list.append(location)
        print('完整图片位置信息获取完成')
        # 有缺口图片
        divs_bg = self.browser.find_elements_by_xpath('//div[@class="gt_cut_bg_slice"]')

        div = divs_bg[0].get_attribute('style')
        # 将后缀替换为jpg
        url = re.findall('url\(\"(.*)\"\);', div)[0].replace('webp', 'jpg')
        # 将图片保存到本地
        response = requests.get(url)
        with open('bg_image.jpg', 'wb') as f:
            f.write(response.content)
        print('有缺口图片下载完成')
        bg_image_location_list = []

        # 获取位置信息
        for div in divs_bg:
            location = {}
            data = div.get_attribute('style')
            location['x'] = int(re.findall('background-position: (.*)px (.*)px;', data)[0][0])
            location['y'] = int(re.findall('background-position: (.*)px (.*)px;', data)[0][1])
            bg_image_location_list.append(location)

        print('有缺口图片位置信息获取完成')
        return full_image_location_list, bg_image_location_list

    def marge_image(self, location_list, image_name):
        """将图片进行重组"""
        # 打开为重组的图片
        name_image = Image.open(image_name)
        # 新建一个空白图片
        new_image = Image.new('RGB', (260, 116))
        # 将没有重组的图片裁剪为小块
        image_upper_list = []  # 上半部分
        image_down_list = []  # 下半部分
        for location in location_list:
            if location['y'] == -58:
                image_upper_list.append(name_image.crop((abs(location['x']), 58, abs(location['x']) + 10, 116)))
            if location['y'] == 0:
                image_down_list.append(name_image.crop((abs(location['x']), 0, abs(location['x']) + 10, 58)))
        # 将裁剪的小块图片粘贴到新的空白图片中
        x_offset = 0
        for im in image_upper_list:
            new_image.paste(im, (x_offset, 0))  # 把小图片放到 新的空白图片上
            x_offset += im.size[0]

        x_offset = 0
        for im in image_down_list:
            new_image.paste(im, (x_offset, 58))
            x_offset += im.size[0]
            new_image.save('full_image.jpg')
        print('%s 重组完成' % image_name)
        return new_image

    def get_distance(self, image1, image2):
        threshold = 60
        for i in range(0, image1.size[0]):  # 260
            for j in range(0, image1.size[1]):  # 160
                pixel1 = image1.getpixel((i, j))
                pixel2 = image2.getpixel((i, j))
                res_R = abs(pixel1[0] - pixel2[0])  # 计算RGB差
                res_G = abs(pixel1[1] - pixel2[1])  # 计算RGB差
                res_B = abs(pixel1[2] - pixel2[2])  # 计算RGB差
                if res_R > threshold and res_G > threshold and res_B > threshold:
                    print('缺口位置确认')
                    return i  # 需要移动的距离

    def get_track(self, distance):

        v = 0  # 初始速度
        t = 0.32  # 单位时间
        track = []  # 存放轨迹
        current = 0  # 当前位置
        mid_distance = distance * 4 / 5
        distance += 5  # 先过一点再滑动回来
        while current < distance:
            if current < mid_distance:
                a = 4.5
            else:
                a = - 5.6
            v0 = v
            s = v0 * t + 1 / 2 * a * t * t
            current += s
            v = v0 + a * t
            track.append(round(s))
        while current > distance:
            move = -random.randint(0, 2)
            current += move
            track.append(round(move))
        for i in range(2):
            track.append(-2)
        for i in range(3):
            track.append(-1)
        print('移动轨迹计算完成')
        return track

    def move(self, track):
        """滑动滑块"""
        print('开始滑动')
        # 定位滑块位置
        size = self.browser.find_element_by_xpath('//*[@id="gc-box"]/div/div[3]/div[2]')
        # 模拟按住鼠标不动
        ActionChains(self.browser).click_and_hold(size).perform()
        # 按照轨迹开始移动
        while track:
            x = track[0]
            ActionChains(self.browser).move_by_offset(xoffset=x, yoffset=0).perform()
            track.remove(x)
        time.sleep(0.5)
        # 放开鼠标
        ActionChains(self.browser).release().perform()
        print('移动完成')

    def login(self):
        """登录"""
        self.open_web_page()
        time.sleep(1)
        self.push_name_password()
        while True:
            try:
                full_image_location_list, bg_image_location_list = self.get_image()
                if full_image_location_list != None and bg_image_location_list != None:
                    image1 = self.marge_image(full_image_location_list, 'full_image.jpg')
                    image2 = self.marge_image(bg_image_location_list, 'bg_image.jpg')
                    distance = self.get_distance(image1, image2)
                    track = self.get_track(distance)
                    self.move(track)
                    time.sleep(5)
                else:
                    print('登录成功')
                    break
            except:
                print('未知错误')
                break
        self.browser.quit()


if __name__ == '__main__':
    bilibil = Bilibili('your user_name ', 'your password')

    bilibil.login()
