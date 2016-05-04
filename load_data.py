import psycopg2
import csv

def main():
    with psycopg2.connect('dbname=test user=alexchescheir host=/tmp') as conn:
        with conn.cursor() as cur:
            cur.execute("select exists(select * from information_schema.tables where table_name=%s)", ('nebraska',))
            if not cur.fetchone()[0]:
                cur.execute("CREATE TABLE nebraska (rank integer, name varchar, " +
                "rush_att integer, rush_yds integer, rush_avg numeric, " +
                "rush_td integer, rec_rec integer, rec_yds integer, " +
                "rec_avg numeric, rec_td integer, scr_plays integer, " +
                "scr_yds integer, scr_avg numeric, scr_td integer, id serial PRIMARY KEY);")
            with open('cfb_schools_nebraska_1983_rushing_and_receiving.csv') as f:
                reader = csv.reader(f)
                next(reader)
                next(reader)
                next(reader)
                for each_player in reader:
                    cur.execute("select exists(select * from nebraska where name='{}')".format(each_player[1]))
                    if not cur.fetchone()[0]:
                        sql_command = "INSERT INTO nebraska VALUES({}, '{}', {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})"
                        cur.execute(sql_command.format(*[0 if x == "" else x for x in each_player]))
    conn.close()

if __name__ == '__main__':
    main()
