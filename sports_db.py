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

def find_name(cur, name):
    cur.execute("select * from nebraska where name='{}'".format(name))
    return cur.fetchall()

def find_min_yards(cur, min_yards):
    cur.execute("select * from nebraska where scr_yds>{}".format(min_yards))
    return cur.fetchall()

def find_yard_range(cur, min_yards, max_yards):
    cur.execute("select * from nebraska where scr_yds between {} and {}".format(min_yards, max_yards))
    return cur.fetchall()

def add_player(cur, name=None):
    to_add = []
    for col in cur.description:
        if col.name == 'name' and name is not None:
            to_add.append(name)
            continue
        elif col.name == 'id':
            continue
        elif col.name.endswith("avg"):
            avg = float(to_add[-1]) / float(to_add[-2])
            to_add.append(avg)
        elif col.name.startswith("scr"):
            scr = sum([int(to_add[-4]),int(to_add[-8])])
            to_add.append(scr)
        else:
            to_add.append(input(col.name + "? "))
    sql_command = "INSERT INTO nebraska VALUES({}, '{}', {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})"
    cur.execute(sql_command.format(*[0 if x == "" else x for x in to_add]))


def main():
    with psycopg2.connect('dbname=test user=alexchescheir host=/tmp') as conn:
        with conn.cursor() as cur:
            search_by_name = input("Would you like to search by name? ")
            if len(search_by_name) == 0 or search_by_name[0].lower() != 'n':
                name = input("What name do you want to search for? ")
                records = find_name(cur, name)
                if len(records) == 0:
                    print("{} is not in the database.".format(name))
                    will_add = input("Would you like to add him? ")
                    if len(will_add) == 0 or will_add.lower()[0] != 'n':
                        add_player(cur, name)
                else:
                    for record in records:
                        print(record)
            else:
                search_by_yards = input("Would you rather search by total yards? ")
                if len(search_by_yards) == 0 or search_by_yards[0].lower() != 'n':
                    min_yards = input("What is the minimum you are interested in? ")
                    records = find_min_yards(cur, min_yards)
                    if len(records) == 0:
                        print("No one had more than {} yards.".format(min_yards))
                        will_add = input("Would you like to add a player? ")
                        if len(will_add) == 0 or will_add.lower()[0] != 'n':
                            add_player(cur)
                    else:
                        print('{} players had more than {} yards.'.format(len(records),min_yards))
                        max_yards = max([x[11] for x in records])
                        print('{} is the max yards.'.format(max_yards))
                    search_max_yards = input("Would you like to add a maximum yards? ")
                    if len(search_max_yards) == 0 or search_max_yards[0].lower() != 'n':
                        max_yards = input("What is the max yards you are interested in? ")
                        records = find_yard_range(cur, min_yards, max_yards)
                        if len(records) == 0:
                            print("No one had between {} and {} yards".format(min_yards, max_yards))
                            will_add = input("Would you like to add a player? ")
                            if len(will_add) == 0 or will_add.lower()[0] != 'n':
                                add_player(cur)
                    if len(records) > 0:
                        for record in records:
                            print(record)
    conn.close()

if __name__ == '__main__':
    main()
