from GardenPi import GardenPi
import sqlite3 as lite


cfg = GardenPi()

dbName = cfg.dbName
con = lite.connect(dbName)
cur = con.cursor()
cur.execute("INSERT INTO events VALUES(null,1,datetime(\'now\'),datetime(\'now\'),11)")
con.commit()
con.close()


print dbName
