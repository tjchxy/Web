# 我这里以实验楼名字缩写命名框架名字： “实验楼 Framework”
from werkzeug.serving import run_simple
from werkzeug.wrappers import Response
from sylfk.wsgi_adapter import wsgi_app
import os
import sylfk.exceptions as exceptions
from sylfk.helper import parse_static_key
from sylfk.route import Route

ERROR_MAP={
    '401': Response('<h1>401 Unknown or unsupported method</h1>', content_type='text/html; charset=UTF-8', status=401),
    '404': Response('<h1>404 Source Not Found<h1>', content_type='text/html; charset=UTF-8', status=404),
    '503': Response('<h1>503 Unknown function type</h1>', content_type='text/html; charset=UTF-8',  status=503)
 }

TYPE_MAP = {
    'css':  'text/css',
    'js': 'text/js',
    'png': 'image/png',
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg'
}

class ExecFunc:
    """docstring for ExecFunc"""
    def __init__(self, func, func_type ,**options):
        self.func = func
        self.options = options
        self.func_type = func_type


class SYLFk:
    # 实例化方法
    def __init__(self,static_folder='static'):
        self.host = '127.0.0.1'
        self.port = 8086
        self.url_map = {}
        self.static_map = {}
        self.function_map = {}
        self.static_folder = static_folder
        self.route=Route(self)

    def dispatch_static(self,static_path):
        if os.path.exists(static_path):
            key=parse_static_key(static_path)
            doc_type=TYPE_MAP.get(key,'text/plain')

            with open(static_path,'rb') as f:
                rep=f.read()
            return Response(rep,content_type=doc_type)
        else:
            return ERROR_MAP['404']



    def add_url_rule(self,url,func,func_type,endpoint=None,**options):
        if endpoint is None:
            endpoint=func.__name__
        if url in self.url_map:
            raise exceptions.URLExistsError
        if endpoint in self.function_map and func_type != 'static':
            raise exceptions.EndpointExistsError
        self.url_map[url]=endpoint
        self.function_map[endpoint]=ExecFunc(func,func_type,**options)




    # 路由
    def dispatch_request(self, request):
        # status = 200  # HTTP状态码定义为 200，表示请求成功

        # # 定义响应报头的 Server 属性
        # headers = {
        #     'Server': 'Shiyanlou Framework'
        # }

        # # 回传实现 WSGI 规范的响应体给 WSGI 模块
        # return Response('<h1>Hello, Framework</h1>', content_type='text/html', headers=headers, status=status)
        # # ...

        # # 框架被 WSGI 调用入口的方法
        url="/"+"/".join(request.url.split("/")[3:]).split("?")[0]
        if url.startswith('/' + self.static_folder + '/'):
            endpoint='static'
            url=url[1:]
        else:
            endpoint=self.url_map.get(url,None)
        headers={'server':'SYL web 0.1'}

        if endpoint is None:
            return ERROR_MAP['404']
        exec_function=self.function_map[endpoint]
        if exec_function.func_type =='route':
            if request.method in exec_function.options.get('methods'):
                argcount=exec_function.func.__code__.co_argcount
                if argcount>0:
                    rep=exec_function.func(request)
                else:
                    rep=exec_function.func()
            else:
                return ERROR_MAP['401']
        elif exec_function.func_type == 'view':
            rep=exec_function.func(request)
        elif exec_function.func_type == 'static':
            return exec_function.func(url)
        else:
            return ERROR_MAP['503']
        status=200
        content_type='text/html'
        return Response(rep,content_type='%s; charset=UTF-8' % content_type,headers=headers,status=status)


    # 启动入口
    def run(self, host=None, port=None, **options):
        for key, value in options.items():
            if value is not None:
                self.__setattr__(key, value)
        if host:
            self.host=host
        if port:
            self.port=port

        self.function_map['static']=ExecFunc(func=self.dispatch_static,func_type='static')
        run_simple(hostname=self.host,port=self.port,application=self,**options)
        # 框架被 WSGI 调用入口的方法
    def __call__(self, environ, start_response):
        return wsgi_app(self, environ, start_response)
