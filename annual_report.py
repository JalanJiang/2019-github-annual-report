import time
import requests

from io import BytesIO
from github4.core import Github
from PIL import Image, ImageDraw, ImageFont


class AnnualReport:

    IMAGE_FILE_PATH = "./img/github.png"

    def __init__(self, github_id):
        self.github_id = github_id
        self.g = Github("替换成你的 access_token")
        self.data = self.get_data()
        
    def get_data(self):
        return self.g.get_user(github_id=self.github_id)

    def check_user_data(self):
        if 'errors' in self.data:
            return False
        else:
            return True

    def get_user_data(self):
        return self.data['data']['user']

    def get_name(self, user):
        # Name 可能是 None
        if user['name'] is None:
            return self.github_id
        return user['name']

    def get_followers(self, user):
        return user['followers']['totalCount']
    
    def get_avatar_url(self, user):
        return user['avatarUrl']

    def get_contribute_data(self, user):
        return user['contributionsCollection']
    
    def get_total_contributions(self, contribute):
        return contribute['contributionCalendar']['totalContributions']

    def get_weeks(self, contribute):
        return contribute['contributionCalendar']['weeks']

    def draw(self):
        f = open(self.IMAGE_FILE_PATH, 'rb')
        image = Image.open(f)
        # 创建一个 draw 实例
        drawImage = ImageDraw.Draw(image)

        # 获取 API 数据
        user_data = self.get_user_data()
        name = self.get_name(user_data)
        followers = self.get_followers(user_data)
        contribute = self.get_contribute_data(user_data)
        total_contributions = self.get_total_contributions(contribute)
        weeks = self.get_weeks(contribute)

        # 数据初始化
        total_day = 0
        max_continue_day = 0 # 最大连续的天数
        continue_day = 0
        pre = False # 前一天的情况
        max_day_contribution_count = 0 # 单天最大次数
        max_day_contribution_date = ''

        # 设置初始位置
        y_begin = 263
        x_point, y_point = 20, y_begin
        square_width = 15
        move_width = 19.5

        # 对周数据循环
        for week in weeks:
            for day in week['contributionDays']:
                contribution_count = day['contributionCount']
                if contribution_count > max_day_contribution_count:
                    max_day_contribution_count = contribution_count
                    max_day_contribution_date = day['date'] # 记录日期

                # 计算连续天数
                if contribution_count == 0:
                    # 今天没有提交记录
                    if pre:
                        # 昨天有提交记录，进行切断
                        max_continue_day = max(max_continue_day, continue_day)
                        continue_day = 0
                    pre = False
                else:
                    # 判断是哪一年
                    if day['date'].split('-')[0] == '2019':
                        # 计算有贡献的天数
                        total_day += 1
                    # 今天有提交记录
                    continue_day += 1
                    pre = True

                # 取出每天的数据
                color = day['color']
                # 绘制图像
                drawImage.line([(x_point, y_point), (x_point + square_width, y_point)], fill=color, width=square_width)
                # y 轴移动
                y_point += move_width
            # x 轴移动
            x_point += move_width
            # y 轴恢复原位置
            y_point = y_begin

        # 连续天数的处理
        max_continue_day = max(max_continue_day, continue_day)

        # 绘制昵称
        font = ImageFont.truetype("./font/hua-wen-hei-ti.ttf", 50) # 微软雅黑字体
        drawImage.text((370, 58), name, fill="#FFFFFF", font=font)

        # 字体初始化
        # 大标题字体设置
        big_title_size = 60
        big_title_font = ImageFont.truetype("./font/fzlt.ttf", big_title_size)
        big_title_color = "#F7CD04"
        # 普通字体设置
        text_size = 30
        text_font = ImageFont.truetype("./font/hua-wen-hei-ti.ttf", text_size)
        text_color = "#F7FFF7"

        # 1. 天数百分比
        left_top_x = 338

        percent = '{:.1%}'.format(total_day / 365)
        percent_w, percent_h = drawImage.textsize(percent, font=big_title_font) # 获取长宽
        drawImage.text((left_top_x - percent_w, 504), percent, fill=big_title_color, font=big_title_font)

        precent_text1 = "你共有 %s 天提交代码" % total_day
        precent_text1_w, percent_text1_h = drawImage.textsize(precent_text1, font=text_font)
        drawImage.text((left_top_x - precent_text1_w, 627), precent_text1, fill=text_color, font=text_font)
        precent_text2 = "占总天数的 %s" % percent
        precent_text2_w, precent_text2_h = drawImage.textsize(precent_text2, font=text_font)
        drawImage.text((left_top_x - precent_text2_w, 667), precent_text2, fill=text_color, font=text_font)

        # 2. 连续天数 todo: 兼容长度
        right_top_x = 770
        max_continue_day = str(max_continue_day)
        drawImage.text((right_top_x, 551), max_continue_day, fill=big_title_color, font=big_title_font)
        max_continue_day_text = "你共有 %s 天" % max_continue_day
        drawImage.text((right_top_x, 640), max_continue_day_text, fill=text_color, font=text_font)

        # 3. 某日最大贡献数
        left_bottom_x = 326

        if max_day_contribution_count == 0:
            # 没有任何贡献
            max_contribution_day_text1 = "你没有提交任何代码"
            max_contribution_day_text2 = "2010 年再多多努力啦"
        else:
            max_day_contribution_date_list = max_day_contribution_date.split("-")
            max_contribution_day_text1 = "%s 年 %s 月 %s 日" % (max_day_contribution_date_list[0], max_day_contribution_date_list[1], max_day_contribution_date_list[2])
            max_contribution_day_text2 = "你完成贡献 %s 次" % max_day_contribution_count

        max_day_contribution_count = str(max_day_contribution_count)
        max_contribution_w, max_contribution_h = drawImage.textsize(max_day_contribution_count, font=big_title_font)
        drawImage.text((left_bottom_x - max_contribution_w, 1598), max_day_contribution_count, fill=big_title_color, font=big_title_font)

        max_contribution_day_text1_w, max_contribution_day_text1_h = drawImage.textsize(max_contribution_day_text1, font=text_font)
        drawImage.text((left_bottom_x - max_contribution_day_text1_w, 1490), max_contribution_day_text1, fill=text_color, font=text_font)
        max_contribution_day_text2_w, max_contribution_day_text2_h = drawImage.textsize(max_contribution_day_text2, font=text_font)
        drawImage.text((left_bottom_x - max_contribution_day_text2_w, 1530), max_contribution_day_text2, fill=text_color, font=text_font)
        # drawImage.text()

        # 4. Followers
        right_bottom_x = 734
        # followers = str(followers)
        followers = format(followers, ',')
        drawImage.text((right_bottom_x, 1598), followers, fill=big_title_color, font=big_title_font)
        follower_text = "%s 位追随者" % followers
        drawImage.text((right_bottom_x, 1543), follower_text, fill=text_color, font=text_font)

        # 5. 中间总贡献数
        total_font_size = 50
        middle_x, middle_y = 542.5, 1068
        total_font = ImageFont.truetype("./font/fzlt.ttf", total_font_size)
        total_contributions = format(total_contributions, ',')
        total_contributions_w, total_contributions_h = drawImage.textsize(total_contributions, font=total_font)
        drawImage.text((middle_x - total_contributions_w / 2, middle_y), total_contributions, fill=text_color, font=total_font)

        # image.show()
        return image