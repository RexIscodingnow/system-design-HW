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


    Return values:
        
        - tuple: 1. First element is a result fetched from the target table.
                 2. Secondly is the length of the fetch result.
    
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

        
        - values: The parameters where sqlite script / command to use.

        >>> values = ['Peter', 'Computer Science', 80]
        
            insert into `students`
            (`name`, `major`, `score`)
            values
            (?, ?, ?)

            It's equivalent to

            insert into `students`
            (`name`, `major`, `score`)
            values
            ('Peter', 'Computer Science', 80)

        - db_path: The database path
        - exe_many: To execute multiple SQL command if it is set to `True`.
    """
    try:
        res_fetch = []
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
                
                * 2 筆資料
            >>> {
                    'name': ('大黃', '小黑'),
                    'email': ('abc@gmail.com', 'black@email.com'),
                    'score': (90, 65)
                }
            
        Example `Users` table:
            
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
           search_vals: Iterable[tuple[str, int | float | str | object]] = [],
           conditions: Iterable[str] = [],
           *,
           fetch_columns: Iterable[int | float | str | object] = [],
           aggregation: dict[str, Iterable[str]] = {}
           ) -> Iterable[int | float | str | object] | None:
    """
    Parameters:
        
        - table_name: 資料表名稱

        - search_vals: 資料表的欄位名稱 + 搜尋資料
                             
            - Explanation: 第一個為欄位名稱，第二個為判斷資料

        >>> [('name', 'John')]

            SELECT * FROM `users` WHERE `name` <condition 1> `John`;
        
        >>> [('name', 'John'), ('score', '90')]

            SELECT * FROM `users`
            WHERE
            `name` <condition 1> `John`
            <condition 2>
            `score` <condition 2> 90 

        - conditions: 條件判斷運算子

        以 [('name', 'John'), ('score', '90')] 為例子，由左至右

        1. '='   : 對應到第一個條件 => ('name', 'John')

        2. 'and' : 兩個條件做 and
        
        3. '>'   : 對應第二個       => ('score', '90')

        >>> ['=', 'and', '>']

        最後指令為  
                    SELECT * FROM `users`
                    WHERE
                    `name` = `John`
                    AND
                    `score` > 90

        
        - fetch_columns: 搜尋的指令欄位

        - aggregation: 聚合函數 (Aggregation function)
        
        >>> {
                "<Aggregation function>" : "<Column name>"
            }

        * 對 score 的資料做排序、計算數量
        >>> {
                "sort": score,
                "count": score
            }

        Example `Users` table:

                    +---------+-----------------+--------+
                    |  name   |      email      | score  |
                    +---------+-----------------+--------+
                    |  John   |  abc@gmail.com  |   90   |
                    +---------+-----------------+--------+
                    |  Emily  | black@email.com |   65   |
                    +---------+-----------------+--------+
    """

    columns = ""

    n = len(fetch_columns)

    if fetch_columns:
        columns = ','.join([f"`{str(col)}`" for col in fetch_columns])
    else:
        columns = "*"

    # select <columns> from <table name> where <conditions>
    # 
    # <conditions> : <column name> < =, <> (not equal), >, <, between, like, in > <value>

    sql_cmd = f"SELECT {columns} FROM `{table_name}`"

    # TODO: test the edge case
    if search_vals and conditions:
        if len(search_vals) > 1 and len(search_vals) == len(conditions):
            print("判斷條件 與 運算子 數目不一致")
            return

        sql_cmd += " WHERE "

        for i, (col, val) in enumerate(search_vals):
            if i > 0:
                sql_cmd += f" {conditions[i]} "
                continue

            sql_cmd += f"`{col}` {conditions[i]} '{val}'"

        if len(search_vals) > 1:
            sql_cmd += f"`{col}` {conditions[i+1]} '{val}'"


    # TODO: aggregation functions
    if aggregation:
        for col, funcs in aggregation.items():
            for func in funcs:
                pass

    print(sql_cmd)
    
    res = exec_cmd_sql(sql_cmd)

    return res


