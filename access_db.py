"""

TODO: 完成 select()

"""


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
    
    print(len(params.values()))
    
    previous = None

    for value in params.values():
        if previous is None:
            previous = value
            continue
        
        if len(previous) != len(value):
            return False
        
        previous = value
        
    return True


def exec_cmd_sql(sql_cmd: str, values: Iterable = [], *, db_path: str = "users.db", exe_many: bool = False):
    """
    Execute the sqlite script or command (one-line or multiple command)
    
    
    Parameters:

        - sql_cmd: SQLite script or command

        >>> insert into `students`
            (`name`, `major`, `score`)
            values
            ('Peter', 'Computer Science', 80)

        >>> insert into `students`
            (`name`, `major`, `score`)
            values
            ('Peter', 'Computer Science', 80), ('Razer', 'Mathematics', 75)

        >>> CREATE TABLE IF NOT EXISTS `users` (
                    `id`        INTEGER         PRIMARY KEY     AUTOINCREMENT,
                    `email`     VARCHAR(100)    UNIQUE          NOT NULL,
                    `password`  VARCHAR(20)     NOT NULL,
            );

        - values: 
    """
    try:
        conn = sqlite3.connect(pathlib.Path(db_path))
        cursor = conn.cursor()

        if exe_many:
            cursor.executemany(sql_cmd, values)
        else:
            cursor.execute(sql_cmd, values)

        res_fetch = cursor.fetchall()
        conn.commit()


    except Exception as e:
        print("SQL command execute error !")
        print(e)


    finally:
        conn.close()

        if len(res_fetch) > 0:
            return res_fetch, len(res_fetch)
        
        else:
            return None, 0


def insert(table_name: str, params: dict[str, Iterable[int | float | str | object | None]]):
    """
    Parameters:
        
        - table_name: 資料表名稱
        
        - params: 插入欄位資料

            * insert columns `name`, `email`, `score`
            * 3 筆資料
            >>> {
                    'name': ('大黃', '小黑'),
                    'email': ('abc@gmail.com', 'black@email.com'),
                    'score': (90, 65)
                }
            
            Users table:
            
                    +--------+-----------------+-------+
                    |  name  |      email      | score |
                    +--------+-----------------+-------+
                    |  大黃  |  abc@gmail.com  |   90  |
                    +--------+-----------------+-------+
                    |  小黑  | black@email.com |   65  |
                    +--------+-----------------+-------+
    """
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
    fields_data: list[Iterable] = []    # for all fields data


    for key, val in params.items():
        columns.append(key)
        fields_data.append(val)
        
        ps += "?,"


    for j in range(len(fields_data[0])):
        for i in range(len(fields_data)):
            insert_data.append(fields_data[i][j])
    

    ps = ps[:-1]
    ps += "),"
    times = len(insert_data) // len(columns)
    
    sql_cmd = f"""
                
                insert into `{table_name}` {tuple(columns)} values {(ps * times)[:-1]}
                
                """.replace("'", '`')
    
    print(sql_cmd, insert_data)
    
    exec_cmd_sql(sql_cmd, insert_data)


def select(table_name: str,
           fields: Iterable[str] = [],
           search_vals: Iterable[int | float | str | object] = [],
           conditions: Iterable[str] = [],
           *,
           aggregation: dict[str, Iterable[str]] = {}
           ) -> Iterable[int | float | str | object] | None:
    """
    Parameters:
        
        - table_name: 資料表名稱

        - fields: 資料表的欄位名稱

        - search_vals: 要搜尋的參數
        
        - aggregation: 聚合函數 (Aggregation function)
        
        >>> {
                "<Column name>" : "<Aggregation function>"
            }

        >>> {
                "score": ["sort", "count"]   # 對 score 的資料做排序、計算數量
            }

            Users table:

                    +---------+-----------------+--------+
                    |  name   |      email      | score  |
                    +---------+-----------------+--------+
                    |  John   |  abc@gmail.com  |   90   |
                    +---------+-----------------+--------+
                    |  Emily  | black@email.com |   65   |
                    +---------+-----------------+--------+
    """
    
    if len(fields) != len(search_vals):
        return None

    columns = ""
    where = ""
    # conditions = {
    #     "equal": "=",
    #     "not-eq": "<>",
    #     "greater": ">",
    #     "less": "<",
    #     "greater-eq": ">=",
    #     "less-eq": "<="
    # }

    if len(fields) > 0:
        for i in range(len(fields)):
            item = fields[i]
            columns += item[0]

            if i < len(fields) - 2:
                columns += ","
    else:
        columns = "*"

    # select <columns> from <table name> where <conditions>
    # 
    # <conditions> : <column name> < =, <> (not equal), >, <, between, like, in > <value>

    cmd = f"select {columns} from {table_name}"
    
    if where != "":
        cmd += f" where {where} "


