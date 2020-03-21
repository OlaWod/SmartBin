import jieba
import pandas as pd

rubbish = dict()
rubbish_data = pd.read_csv('./assets/rubbish.csv', encoding='gbk')

r = list(rubbish_data["可回收物"])
r = dict.fromkeys(r, '可回收物')
rubbish.update(r)

r = list(rubbish_data["有害垃圾"])
r = dict.fromkeys(r, '有害垃圾')
rubbish.update(r)

r = list(rubbish_data["厨余垃圾"])
r = dict.fromkeys(r, '厨余垃圾')
rubbish.update(r)

r = list(rubbish_data["其他垃圾"])
r = dict.fromkeys(r, '其他垃圾')
rubbish.update(r)



def get_type(string):
    
    seg_list = jieba.cut(string, cut_all=True)  # 全模式
    
    for x in seg_list:
        if x in rubbish:
            return x,rubbish[x]
        
    return False





if __name__=='__main__':    # 模块测试

    string = "废纸是什么垃圾"

    result = get_type(string)
    
    if result==False:   # 没有说任何垃圾
        print('你没说到垃圾')
    else:
        print(result[0]+'是'+result[1])
