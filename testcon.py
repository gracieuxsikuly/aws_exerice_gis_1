from db import get_connection
try:
    con=get_connection()
    cur=con.cursor()
    cur.execute("SELECT VERSION();")
    print(cur.fetchone())
    cur.close()
    con.close()
except Exception as e:
    print("Erreur de connexion:",e)
