import sqlite3

def print_all_fmp_rows(db_path: str = "comp6231.sqlite3"):
    # 1. 建立连接
    conn = sqlite3.connect(db_path)
    # 如果想要以字典方式访问列名，可以启用 row_factory：
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    # 2. 执行查询
    cursor.execute("SELECT * FROM FMP;")
    rows = cursor.fetchall()

    # 3. 打印结果
    # ——方式 A：按元组打印
    for row in rows:
        print(tuple(row))

    # ——方式 B：按列名打印（需要启用 row_factory）
    # for row in rows:
    #     print({key: row[key] for key in row.keys()})

    # 4. 关闭连接
    cursor.close()
    conn.close()

if __name__ == "__main__":
    print_all_fmp_rows()
