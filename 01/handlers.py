# -*- coding:utf-8 -*-

class Handle(object):
    '调用方法的处理类'

    # 判断当前类是否有对应的方法，所有的话则根据提供的额外参数使用对应方法
    def callback(self, prefix, name, *args):
        method = getattr(self, prefix+name, None)
        if callable(method):
            return method(*args)

    # callback的辅助方法，前缀就是start，只需要提供方法名即可
    def start(self, name):
        self.callback('start_', name)
    # 前缀为end的callback辅助方法
    def end(self, name):
        self.callback('end_', name)

    #返回方法substitution
    def sub(self, name):
        def substitution(match):
            result = self.callback('sub_', name, match)
            if result is None:
                result =  match.group(0)
            return result
        return substitution

class HTMLRender(Handle):
    '''
    继承自Handle
    '''

    def start_document(self):
        print '<html><head><title>...</title></head><body>'

    def end_document(self):
        print '</body></html>'

    def start_paragraph(self):
        print '<p>'

    def end_paragraph(self):
        print '</p>'

    def start_heading(self):
        print '<h2>'

    def end_heading(self):
        print '</h2>'

    def start_list(self):
        print '<ul>'

    def end_list(self):
        print '</ul>'

    def start_listitem(self):
        print '<li>'

    def end_listitem(self):
        print '</li>'

    def start_title(self):
        print '<h1>'

    def end_title(self):
        print '</h1>'

    def sub_emphasis(self, match):
        return '<em>%s</em>' % match.group(1)

    def sub_url(self, match):
        return '<a href="%s">%s</a>' % (match.group(1), match.group(1))

    def sub_mail(self, match):
        return '<a href="mailto:%s">%s</a>' % (match.group(1), match.group(1))

    def feed(self, data):
        print data
