#在字段计算器中使用

import itertools

counter = itertools.count(start=1)  # 设置计数器起始值

def generate_id():
    return next(counter)  # 使用 next 函数获取下一个计数器值

generate_id()