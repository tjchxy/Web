# 我这里以实验楼名字缩写命名框架名字： “实验楼 Framework”
from werkzeug.serving import run_simple
from werkzeug.wrappers import Response
from sylfk.wsgi_adapter import wsgi_app

class SYLFk:

    # 实例化方法
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 8086

    # 路由
    def dispatch_request(self, request):
        status = 200  # HTTP状态码定义为 200，表示请求成功

        # 定义响应报头的 Server 属性
        headers = {
            'Server': 'Shiyanlou Framework'
        }

        # 回传实现 WSGI 规范的响应体给 WSGI 模块
        return Response('<h1>Hello, Framework</h1>', content_type='text/html', headers=headers, status=status)
        # ...

        # 框架被 WSGI 调用入口的方法

    def __call__(self, environ, start_response):
        return wsgi_app(self, environ, start_response)

    # 启动入口
    def run(self, host=None, port=None, **options):
        for key, value in options.items():
            if value is not None:
                self.__setattr__(key, value)
        if host:
            self.host=host
        if port:
            self.port=port
        run_simple(hostname=self.host,port=self.port,application=self,**options)

        # 框架被 WSGI 调用入口的方法
    def __call__(self, environ, start_response):
        return wsgi_app(self, environ, start_response)
