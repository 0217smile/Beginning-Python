#encoding:utf-8
class Rule:
    def action(self,block,handler):
        handler.start(self.type)
        handler.feed(block)
        handler.end(self.type)
        return True

class HeadingRule(Rule):
    '''
      标题占一行，不包含\n，最多70个字符，并且不以冒号结尾
    '''
    type = 'heading'
    def condition(self,block):
        return not '\n' in block and len(block) <=70 and not block[-1] == ':'

class TitleRule(HeadingRule):
    '''
    题目是文档的第一个块，但前提是它是大标题。只工作一次，处理第一个快，因为处理完一次之后first的值被设置为了False，所以不会再执行处理方法了
    '''
    type = 'title'
    first = True
    def condition(self,block):
        if not self.first: return False
        self.first = False
        return HeadingRule.condition(self,block)

class ListItemRule(Rule):
    '''
    列表项是以连字符开始的段落。作为格式化的一部分，要移除连字符
    '''
    type = 'listitem'
    def condition(self,block):
        return block[0] == '-'
    def action(self,block,handler):
        handler.start(self.type)
        handler.feed(block[1:].strip())
        handler.end(self.type)
        return True

class ListRule(ListItemRule):
    '''
    列表从不是列表项的块和随后的列表项之间。在最后一个连续列表项之后结束
    这里定义了一个变量inside为True，我们可以理解这个变量的意思是—List列表开始。
    因为在html中List中还会包含节点，也就是这里的ListItem,所以他会在遇到一个列表项的时候触发一次，然后在最后一个列表项的时候再次触发。
    所以inside作为一个标志位，用来进行判断符合规则的文本块时需要执行start还是end方法。
    列表匹配的块是这样的：
    <ul>
    <li>What is SPAM?(<a href="http://wwspam.fu/whatisspam">http://wwspam.fu/whatisspam</a>)</li>
    <li>How do they make it?(<a href="http://wwspam.fu/howtomakeit">http://wwspam.fu/howtomakeit</a>)</li>
    <li>Why should I eat it?(<a href="http://wwspam.fu/whyeatit">http://wwspam.fu/whyeatit</a>)</li>
    </ul>
    '''
    type = 'list'
    inside = False
    def condition(self,block):#这个也默认是True
        return True
    def action(self,block,handler):
        if not self.inside and ListItemRule.condition(self,block):#首个列表项本身既是列表项，也是列表开始的标志。可以这样考虑的。
            handler.start(self.type)
            self.inside = True
        elif self.inside and not ListItemRule.condition(self,block):
            handler.end(self.type)
            self.inside = False
        return False

class ParagraphRule(Rule):
    type = 'paragraph'
    def condition(self,block):
        return True