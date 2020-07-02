import os
# "db" 这里 填写db文件与当前代码文件父目录的相对位置
# db_path 是绝对路径
db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "csv")
print(db_path+'/bbb')