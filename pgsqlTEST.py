import psycopg2

conn = psycopg2.connect(database="jspro_test",user="jspro",password="AglbCVss",host="10.0.10.77",port="5432")
cur = conn.cursor()

cur.execute("select * from t_modelrule_model_classify where ftenant_id = '39ca61dfcfac43dca8d5cdb0f1cfddf1'")

#获取结果集的每一行
rows = cur.fetchall()
# print(len(rows))
# print(rows[11][12])

#获取所有字段名
all_fields = cur.description

# field_messages = []

# for i in range(len(all_fields)):
#     # 格式化输出结果，len参数是各列的显示宽度，可以指定常量，也可自定义函数进行获取
#     field_messages.append("{str:<{len}}".format(str=str(all_fields[i][0]),len=50))
#
# field_message = "".join(field_messages)
# print(field_message)

# 然后逐行打印结果集
# for row in rows:
#     row_messages = []
#     for j in range(len(row)):
#         row_messages.append("{str:<{len}}".format(str=str(row[j]),len=50))
#     row_message = "".join(row_messages)
#     print(row_message)
row_minid = []
def find_next(parent_id):
    row_minidb = []
    row_ida =[]
    for parent_idb in parent_id:
        row_idb = []
        for i in range(len(rows)):
            if rows[i][10] == 0 and rows[i][12] == parent_idb:
                row_idb.append(rows[i][0])
                row_ida.append(rows[i][0])
        if len(row_idb) == 0:
            row_minidb.append(parent_idb)
    return row_ida,row_minidb

row_ida = ["rootid"]
while len(row_ida):
    row_ida, row_minida = find_next(row_ida)
    row_minid = row_minid + row_minida

print(row_minid)


# parent_id = ["7e9dcd7d54bc4fc694b50c7de0f60893"]
# print(find_next(parent_id))
# print(row_minid)



conn.close()