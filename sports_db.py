import psycopg2

# class db_manager: #
#     def __init__(self, db_name, user_name='alexchescheir'):
#         self.db_name = db_name
#         self.user_name = user_name
#
#     def __enter__(self):
#         self.conn = psycopg2.connect("dbname={} user={} host=/tmp/".format(
#             self.db_name, self.user_name))
#         self.cur = self.conn.cursor()
#         return self.cur
#
#     def __exit__(self, type, value, traceback):
#         # self.cur.close()
#         # self.conn.close()
#         pass

def main():
    with psycopg2.connect('dbname=test user=alexchescheir host=/tmp') as conn:
        with conn.cursor() as cur:
            pass
    conn.close()
    
if __name__ == '__main__':
    main()
