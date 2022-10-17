import pymysql
import pandas as pd
import os,json

def get_json_data(path):
    try:
        with open(path, 'rb') as f:
            params = json.load(f)
        f.close()
        return params
    except:
        return {}

def write_json_data(path,dict):
    with open(path, 'w',encoding='utf-8') as r:
        json.dump(dict, r,ensure_ascii=False,indent= 4)
    r.close()


def mkcsv():
    jsondata = get_json_data("conf/setting.json")
    db_ip = jsondata["db_ip"]
    db_port = jsondata["db_port"]
    db_user = jsondata["db_user"]
    db_passwd = jsondata["db_passwd"]
    db_database = jsondata["db_database"]
    mk_all_list = jsondata["mk_all_list"]
    singlesqllist = jsondata["singlesqllist"]

    conn = pymysql.connect(host=db_ip, port=db_port, user=db_user, password=db_passwd, database=db_database,
                                 charset="GB2312")
    if os.path.exists("csvlist"):
        pass
    else:
        os.makedirs("csvlist")

    for tablename in mk_all_list:
        try:
            df = pd.read_sql(f"select * from {tablename}",conn)
            df.to_csv(path_or_buf=f"csvlist/{tablename}.csv",encoding="GB2312",index=0)
            print(f"{tablename} mkcsv success")
        except Exception as e:
            print(tablename,"mkerr : ",e)

    for key in singlesqllist:
        try:
            df = pd.read_sql(singlesqllist[key],conn)
            df.to_csv(path_or_buf=f"csvlist/{key}.csv",encoding="GB2312",index=0)
            print(f"{key} mkcsv success")
        except Exception as e:
            print(key,"mkerr : ",e)

    input("生成结束,按任意键退出")