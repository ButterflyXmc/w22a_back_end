import mariadb
import dbcreds

def connect_db():
    try:
        conn = mariadb.connect(
                user = dbcreds.user,
                password = dbcreds.password,
                host = dbcreds.host,
                port = dbcreds.port,
                database = dbcreds.database,
                autocommit = True
            )
        cursor = conn.cursor()
        return cursor
    except mariadb.OperationalError as e:
        print("OPERATIONAL ERROR : ", e)
    except Exception as e:
        print("UNEXPECTED ERROR : ", e)

def disconnect_db(cursor):
    try:
        conn = cursor.connection
        cursor.close()
        conn.close()
    except mariadb.OperationalError as e:
        print("OPERATIONAL ERROR : ", e)
    except mariadb.InternalError as e:
        print("INTERNAL ERROR : ", e)
    # ^ These two errors will pop up if conncting to db is not successful
    except Exception as e:
        print("UNEXPECTED ERROR : ", e)
    # ^ If aythingg else goes wrong


#! This function will receive a valid sql statement and run it
# return str(e) - > returning the error as a string specifically for whoever is using the api
def execute_statement(cursor, statement, args=[]):
    try:
        cursor.execute(statement, args)
        results = cursor.fetchall()
        return results
    except mariadb.ProgrammingError as e:
        if "doesn't have a result set" in e.msg:
            return None
        print ("Syntax error in your sql statement:", e)
        return str(e)
    except mariadb.IntegrityError as e:
        print("The statement failed to execute due to integrity error:",e)
        return str(e)
    except mariadb.DataError as e:
        print("DATA ERROR:", e)
        return str(e)
    except Exception as e:
        print("Soemthing went wrong:",e)
        return str(e)


def run_statement(statement : str, args=[]):
    cursor = connect_db()
    if (cursor == None):
        print("Failed to connect to the DB, statement will not run")
        return None
    result = execute_statement(cursor, statement, args)
    disconnect_db(cursor)
    return result