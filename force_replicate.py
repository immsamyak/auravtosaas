import psycopg2

conn = psycopg2.connect("postgres://postgres:9b97a0a647900bba@147.93.109.117:5432/aura_db")
cur = conn.cursor()

cur.execute("UPDATE core_globalsettings SET vto_engine = 'replicate' WHERE id = 1;")
conn.commit()

cur.execute("SELECT vto_engine FROM core_globalsettings WHERE id = 1;")
print(cur.fetchone())

cur.close()
conn.close()
