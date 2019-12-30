'''
@Description: 核心类
@Version: v1.0
@Author: JalanJiang
@Date: 2019-10-12 10:37:25
@LastEditTime : 2019-12-30 10:37:26
'''
import json
from datetime import datetime

from github4.tools.request import Request

class Github:

    BASE_URL = "https://api.github.com/graphql"

    def __init__(self, access_token=None):
        '''
        @description: 构造函数
        @param access_token: Github AccessToken 
        @return: None
        '''
        self.access_token = access_token
        self.request = Request(access_token=self.access_token)
        
    def get_user(self, github_id):
        '''
        @description: 查询用户数据
        @param : 
        @return: 
        '''
        begin = datetime(2018, 12, 30, 0, 0).isoformat()
        end = datetime(2019, 12, 29, 0, 0).isoformat()
        query = """
        {
            user(login: "%s") {
                followers {
                    totalCount
                }
                avatarUrl
                bio
                name
                contributionsCollection(
                    from: "%s",
                    to: "%s"
                ) {
                    contributionCalendar {
                        totalContributions
                        weeks {
                            contributionDays {
                                color
                                contributionCount
                                date
                                weekday
                            }
                            firstDay
                        }
                    }
                }
            }
        } 
        """% (github_id, begin, end)
        data = self.request.query_request(query=query)
        # print(data)
        return data
