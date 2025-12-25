import pandas as pd
import os

def gen_pivot_table(path, index, values):
    print("开始")
    data = pd.read_excel(path)
    pivot_table = pd.pivot_table(data, index=index, values=values, aggfunc=lambda x: '；'.join(x.astype(str)))
    pivot_table[values[0]] = pivot_table[values[0]].apply(lambda x: "；".join(list(set(x.split('；')))))
    # 可增加更多的值列处理
    pivot_table.to_excel(os.path.join(os.path.dirname(path), os.path.basename(path).split('.')[0]+'_output.xlsx'))
    print("完成")


if __name__ == "__main__":
    # 输入文件路径
    path = r"D:\导出结果.xlsx"
    # 要汇总的列
    index = ["列1"]
    # 要汇总的值
    values = ["列2"]
    gen_pivot_table(path, index, values)