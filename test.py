# -*- coding: utf-8 -*-

class Stack:
    def __init__(self):# 创建一个空的新栈
        self.items = []
    def push(self,item):
        # 尾部[1]顶部
        # [1,2]
        # [1,2,3]
        self.items.append(item) # 将一个新项添加到栈的顶部
    def pop(self):
        return self.items.pop() # 从栈中删除顶部项，栈被修改
    def peek(self):
        return self.items[-1:][0] # 从栈返回顶部项，但不会删除它
    def isEmpty(self):
        return self.items == [] # 测试栈是否为空，返回布尔值
    def size(self):
        return len(self.items) # 判断栈中元素的数量，返回一个整数
# a = Stack()
# a.push(1)
# a.push(2)
# a.push(3)
# print(a.peek())
# print(a.items)


