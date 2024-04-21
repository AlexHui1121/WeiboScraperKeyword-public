# encoding: utf-8


class IPProxyMiddleware(object):
    """
    代理IP中间件
    """
    
    @staticmethod
    def fetch_proxy():
        """
        获取一个代理IP
        """
        # You need to rewrite this function if you want to add proxy pool
        # the function should return an ip in the format of "ip:port" like "12.34.1.4:9090"
        return None

    def process_request(self, request, spider):
        """
        将代理IP添加到request请求中
        """
        
        proxy_data = self.fetch_proxy()
        # proxy_data = '60.182.184.172:8888'
        if proxy_data:
            current_proxy = f'http://{proxy_data}'
            spider.logger.debug(f"current proxy:{current_proxy}")
            request.meta['proxy'] = current_proxy
            
            
            
    # def process_request(self, request, spider):
    #     proxy = "tps125.kdlapi.com:15818"
    #     request.meta['proxy'] = "http://%(proxy)s" % {'proxy': proxy}
    #     # 用户名密码认证
    #     username = <你的用户名>
    #     password= <你的密码>
    #     request.headers['Proxy-Authorization'] = basic_auth_header(username, password)  # 白名单认证可注释此行
    #     request.headers['Accept-Encoding']='gzip'
    #     return None
