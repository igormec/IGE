import sqlite3

maindb = sqlite3.connect('C:/Users/Igor/Documents/Dev/projects/IGE/db/MAIN.db')
mainCur = maindb.cursor()


def create_db(name):
    conn = sqlite3.connect("C:/Users/Igor/Documents/Dev/projects/IGE/db/"+name+".db")
    c = conn.cursor()

    c.execute("CREATE TABLE  "+name+" (id, username, full_name, profile_pic_url, is_verified, followed_by_viewer, requested_by_viewer)")

    conn.commit()
    conn.close()

    
    
c.execute("SELECT * FROM following WHERE (username LIKE '%bern%') OR (full_name LIKE '%bern%')")
rows = c.fetchall()
