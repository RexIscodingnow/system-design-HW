import sqlite3
import pathlib

from typing import Iterable


def checkLength(params: dict[str, Iterable[int | float | str | object | None]]) -> bool:
    """
    Check length.

    Return `True` if all the lengths of insert data from `params` are same size.
    Otherwise, return False.
    

    Parameters:

        -- parame: 插入欄位資料
    """
    
    if params is None or len(params.items()) == 0:
        return False
    
    previous = None

    for value in params.values():
        if previous is None:
            previous = value
            continue
        
        if len(previous) != len(value):
            return False
        
        previous = value
        
    return True


def exec_cmd_sql(sql_cmd: str, values: Iterable = [], exe_many = False):
    try:
        conn = sqlite3.connect(pathlib.Path("users.db"))
        cursor = conn.cursor()

        if exe_many:
            cursor.executemany(sql_cmd, values)
        else:
            cursor.execute(sql_cmd, values)

        conn.commit()


    except Exception as e:
        print("SQL command execute error !")
        print(e)


    finally:
        conn.close()


def insert(table_name: str, params: dict[str, Iterable[int | float | str | object | None]]):
    """
    Parameters:
        
        -- table_name : 資料表名稱
        
        -- params : 插入欄位資料

            * insert columns `name`, `email`, `score`
            * 3 筆資料
            >>> {
                    'name': ('大黃', '小黑'),
                    'email': ('abc@gmail.com', 'black@email.com'),
                    'score': (90, 65)
                }
    """
    # TODO: 測試插入狀態
    if checkLength(params) == False:
        print("插入的數量不一致")
        return
    

    # ps = (?, ?, ...)  =>  ? 號的數量，代表要插入欄位的數量
    # 
    # ps = (?, ?)  代表要插入 2 個欄位
    # 
    ps = "("
    columns = []
    insert_data = []
    
    for key, val in params.items():
        columns.append(key)
        
        for item in val:
            insert_data.append(item)
        
        ps += "?,"

    ps = ps[:-1]
    ps += "),"
    times = len(insert_data) // len(columns)
    
    sql_cmd = f"""
                
                insert into `{table_name}` {tuple(columns)} values {(ps * times)[:-1]}
                
                """.replace("'", '`')
    
    print(sql_cmd, insert_data)
    
    exec_cmd_sql(sql_cmd, insert_data)


def select(table_name: str,
           fields_queryItems: Iterable[tuple[str, int | float | str | object | None]] = [],
           params: dict[str, str] = {},
           ):
    """
    Arguments:
        
        -- table_name: 資料表名稱
        
        -- params: 聚合函數
        >>> {"sort": field_name}
    """
    columns = ""
    where = ""
    conditions = {
        "equal": "=",
        "not-eq": "<>",
        "greater": ">",
        "less": "<",
        "greater-eq": ">=",
        "less-eq": "<="
    }

    if len(fields_queryItems) > 0:
        for i in range(len(fields_queryItems)):
            item = fields_queryItems[i]
            columns += item[0]

            if i < len(fields_queryItems) - 2:
                columns += ", "
    else:
        columns = "*"

    # select <columns> from <table name> where <conditions>
    # 
    # <conditions> : <column name> < =, <> (not equal), >, <, between, like, in > <value>

    cmd = f"select {columns} from {table_name}"
    
    if where != "":
        cmd += f" where {where} "


