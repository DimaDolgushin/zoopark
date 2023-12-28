import sqlite3
import os
from settings import DB_PATH


class DBManager:

    def __init__(self, db_path) -> None:
        self.db_path = db_path

    def db_connect(self) -> tuple[sqlite3.Connection, sqlite3.Cursor]:
        connect = sqlite3.connect(self.db_path)
        cursor = connect.cursor()
        return connect, cursor

    def check_base(self) -> bool:
        return os.path.exists(path=self.db_path)

    def execute_script(self, file) -> dict:
        connect, cursor = self.db_connect()
        try:
            res = cursor.executescript(open(file=file).read())
            connect.commit()
            return {"code": 200, "message": "Ok!", "result": res}
        except sqlite3.Error as ex:
            connect.close()
            return {"code": 400, "message": f"Sqlite3 error - ~{ex}~", "result": None, }
        except sqlite3.IntegrityError as ex:
            connect.close()
            return {"code": 400, "message": f"Integrity error - ~{ex}~'", "result": None}
        except sqlite3.ProgrammingError as ex:
            connect.close()
            return {"code": 400, "message": f"Programming error - ~{ex}~", "result": None}
        except sqlite3.OperationalError as ex:
            connect.close()
            return {"code": 400, "message": f"Operational error - ~{ex}~", "result": None}
        finally:
            connect.close()

    def create_base(self, file: str) -> dict:
        if not self.check_base():
            return self.execute_script(file=file)

    def execute_query(self, query: str, args: tuple = (), fetch_one: bool = True) -> dict:
        connect, cursor = self.db_connect()
        try:
            res = cursor.execute(query, args)
            if fetch_one:
                res = res.fetchone()
            else:
                res = res.fetchall()
            connect.commit()
            return {"code": 200, "message": "Ok!", "result": res}
        except sqlite3.Error as ex:
            connect.close()
            return {"code": 400, "message": f"Sqlite3 error - ~{ex}~", "result": None, }
        except sqlite3.IntegrityError as ex:
            connect.close()
            return {"code": 400, "message": f"Integrity error - ~{ex}~'", "result": None}
        except sqlite3.ProgrammingError as ex:
            connect.close()
            return {"code": 400, "message": f"Programming error - ~{ex}~", "result": None}
        except sqlite3.OperationalError as ex:
            connect.close()
            return {"code": 400, "message": f"Operational error - ~{ex}~", "result": None}
        finally:
            connect.close()


base_worker = DBManager(db_path=DB_PATH)
