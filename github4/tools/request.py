'''
@Description: 请求工具
@Version: v1.0
@Author: JalanJiang
@Date: 2019-10-12 11:05:34
@LastEditTime: 2019-12-11 16:58:21
'''
import json
import requests


class Request:

    BASE_URL = "https://api.github.com/graphql"

    def __init__(self, access_token): 
        '''
        @description: 构造函数
        @param access_token: Github AccessToken 
        @return: None
        '''
        self.headers = {"Authorization": "bearer %s" % access_token}

    def query_request(self, query):
        '''
        @description: 发送请求
        @param query: JSON 结构体
        @return: 字典结构数据结果
        '''
        res = requests.post(
            Request.BASE_URL,
            headers=self.headers,
            json={'query': query}
        )
        # 返回字典结构数据
        return json.loads(res.content.decode())