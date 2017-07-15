# encoding:utf-8
import sys, re
from handlers import *
from util import *
from rules import *


class Parser:
    # 初始化一些属性
    def __init__(self, handler):
        self.handler = handler
        self.rules = []
        self.filters = []

    # 向规则列表中添加规则
    def addRule(self, rule):
        self.rules.append(rule)

    # 向过滤器列表中添加过滤器
    def addFilter(self, pattern, name):
        # 创建过滤器，实际上这里return的是一个替换式
        def filter(block, handler):
            return re.sub(pattern, handler.sub(name), block)

        self.filters.append(filter)

    # 对文件进行处理
    def parse(self, file):
        self.handler.start('document')
        # 对文件中的文本块依次执行过滤器和规则
        for block in blocks(file):
            for filter in self.filters:
                #每个filter都要过一遍，（其实每个filter就是个方法），
                # 看block中是否有emphasis,url,email的，有则进行替换，返回替换后的block。没有的话直接把block返回
                block = filter(block, self.handler)
            for rule in self.rules:
                # 判断文本块是否符合相应规则，若符合做执行规则对应的处理方法
                # 其实每个rule是ListRule(),ListItemRule()等，这些类
                if rule.condition(block):
                    last = rule.action(block, self.handler)
                    if last: break
        self.handler.end('document')


class BasicTextParser(Parser):
    def __init__(self, handler):
        Parser.__init__(self, handler)
        #添加规则的顺序很重要
        self.addRule(ListRule())    #ListRule()是返回False的
        self.addRule(ListItemRule())
        self.addRule(TitleRule()) #TitleRule()继承自HeadingRule()类
        self.addRule(HeadingRule())
        self.addRule(ParagraphRule()) #ParagraphRule()类的条件判断默认是True，所以它放在最后，用来处理其他规则没有覆盖到的block

        self.addFilter(r'\*(.+?)\*', 'emphasis')
        self.addFilter(r'(http://[\.a-zA-Z/]+)', 'url')
        self.addFilter(r'([\.a-zA-Z]+@[\.a-zA-Z]+[a-zA-Z]+)', 'mail')


handler = HTMLRender()
parser = BasicTextParser(handler)

parser.parse(sys.stdin)