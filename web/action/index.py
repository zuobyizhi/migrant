# -*- coding:utf-8 -*- 
"""
    author comger@gmail.com
    migrant 前端展示公共页面
"""
from kpages import url
from kpages.context import get_context
from logic.account import active_account, apply_active_account
from utility import BaseHandler


@url(r'/?')
class Index(BaseHandler):
    def get(self):
        self.render('action/index.html')


@url(r'/login?')
class Login(BaseHandler):
    def get(self):
        self.render('action/login.html')


@url(r'/logout?')
class Logout(BaseHandler):
    def get(self):
        self.clear_cookie('uid')
        self.clear_cookie('city')
        self.redirect('/')


@url(r'/profile?')
class Profile(BaseHandler):
    def get(self):
        self.render('action/profile.html')


@url(r'/setpwd?')
class SetPwd(BaseHandler):
    def get(self):
        self.render('action/setpwd.html')


@url(r'/checkmail?')
class CheckMail(BaseHandler):
    """
    1. 用户注册成功 ./checkmail?username=xxx@xxx.com
    2. 用户登录，账号未激活 ./checkmail?username=xxx@xxx.com
    3. 用户点击激活链接 checkmail?key=xxxxxxxxxx
    """
    def get(self):
        key = self.get_argument('key', None)
        username = self.get_argument('username', None)
        frm = self.get_argument('from', None)
        kwargs = {
            'key': key,
            'username': username,
            'frm': frm
        }
        template_file = 'action/check_email.html'

        if not key:
            # 注册成功、登录失败
            r, v = apply_active_account(username,self.request.host)

            if frm and frm == 'resend':
                self.write(dict(status=r, data=v))
            else:
                kwargs.update(username=username, status=r, data=v)
                self.render(template_file, **kwargs)
        else:
            # 点击邮件激活链接
            r, v = active_account(key)
            kwargs.update(key=key, status=r, data=v)
            self.render(template_file, **kwargs)

    def post(self):
        self.get()


@url(r'/forgot_password?')
class ForgotPassword(BaseHandler):
    def get(self):
        key = self.get_argument('key', None)
        kwargs = {
            'key': None,
            'expired': False
        }
        template_file = 'action/forget_password.html'
        if not key:
            self.render(template_file, **kwargs)
        else:
            redis = get_context().get_redis()
            username = redis.get(key)
            if username:
                kwargs.update(key=key)
                self.render(template_file, **kwargs)
            else:
                kwargs.update(expired=True)
                self.render(template_file, **kwargs)
