import sqlite3
def record():
    
    file_1 = open(r'D:\Python(Pycharm)\untitled\Fireball\record_level.txt', 'r')
    file_2 = open(r'D:\Python(Pycharm)\untitled\Fireball\record_levels.txt', 'r')
    
    record_total = file_1.readline()
    list_total=[]
    for line in file_2:
        if line=='\n':
            continue
        list_total.append(line)
    
    list_total.append(record_total)
    file_1.close()
    file_2.close()
    file_2 = open(r'D:\Python(Pycharm)\untitled\Fireball\record_levels.txt', 'w')
    for i in list_total:
        file_2.write(i + '\n')
    file_2.close()
def record_2():
    conn = sqlite3.connect('subbota.sqlite')
    cursor = conn.cursor()
    file_1 = open(r'D:\Python(Pycharm)\untitled\Fireball\record_in_file.txt', 'r')
    file_2 = open(r'D:\Python(Pycharm)\untitled\Fireball\record_levels.txt', 'r')
    list_for_name = []
    list_for_total = []
    for line in file_1:
        if line == '\n':
            continue
        list_for_name.append(line)
    for line in file_2:
        if line == '\n':
            continue
        list_for_total.append(line)
    new_list_for_name = ''
    for i in range(len(list_for_name)):
        try:
            new_list_for_name += list_for_name[i]
        except IndexError:
            break
    list_for_name = new_list_for_name.split('\n')
    list_for_name.pop(-1)
    i = 0
    while (True):
        try:
            cursor.execute('insert into fireball values(?,?)', (list_for_total[i], list_for_name[i]))
            i += 1
        except IndexError:
            break
    cursor.execute("SELECT * FROM fireball ORDER BY  total DESC ")
    results = cursor.fetchall()
    conn.close()
    return (results)