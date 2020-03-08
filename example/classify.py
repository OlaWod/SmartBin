import jieba
import mysql.connector


mydb = mysql.connector.connect(
  host="localhost",       # 数据库主机地址
  user="root",    # 数据库用户名
  passwd="root",   # 数据库密码
  database="rubbish"
)
 
mycursor = mydb.cursor()



def get_type(string):
    
    seg_list = jieba.cut(string, cut_all=True)  # 全模式
    
    for x in seg_list:
        mycursor.execute("SELECT type FROM rubbishs where name='"+x+"'")
        myresult = mycursor.fetchall()
        
        if myresult!=[]:
            return x,myresult[0][0]
        
    return False





if __name__=='__main__':    # 模块测试

    string = "废纸是什么垃圾"

    result = get_type(string)
    
    if result==False:   # 没有说任何垃圾
        print('你没说到垃圾')
    else:
        print(result[0]+'是'+result[1])
