import psycopg2
import psycopg2.extras as extras


# host.docker.internal , host name for docker
# localhost , host name for script.py

class Connection:
    create_table = ''' CREATE TABLE IF NOT EXISTS measurement (
                                 period_start    varchar(40),
                                 period_end  varchar(40),
                                 N  int,
                                 min  float8,
                                 max  float8,
                                 median  float8,
                                 average  float8) '''

    drop_table = "DROP TABLE IF EXISTS measurement"

    insert_query = "INSERT INTO %s(%s) VALUES %%s"

    is_exists = '''SELECT EXISTS (
                         SELECT FROM 
                             pg_tables
                         WHERE 
                             schemaname = 'measurementsdb' AND 
                             tablename  = 'measurement');'''

    def __init__(self, host='localhost',
                 dbname='measurementsdb',
                 user='postgres',
                 password='admin',
                 port=5432):
        self.conn = psycopg2.connect(host=host, dbname=dbname, user=user, password=password, port=port)

    def close_connection(self):
        self.conn.close()

    def insert_data(self, data):
        try:
            with self.conn.cursor() as cur:
                if cur.execute(self.is_exists):
                    cur.execute(self.drop_table)
                    cur.execute(self.create_table)
                    print("measurement table created")

                tuples = [tuple(x) for x in data.to_numpy()]
                cols = ','.join(list(data.columns))

                query = self.insert_query % ("measurement", cols)
                extras.execute_values(cur, query, tuples)

                print("values inserted")
                self.conn.commit()

        except Exception as error:
            self.conn.rollback()
            print(error)

        finally:
            cur.close()
