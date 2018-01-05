import sqlite3

#maindb = sqlite3.connect('C:/Users/Igor/Documents/Dev/projects/IGE/db/MAIN.db')
#c = maindb.cursor()


def create_db(name):
    conn = sqlite3.connect("C:/Users/Igor/Documents/Dev/projects/IGE/db/"+name+".db")
    c = conn.cursor()

    c.execute("CREATE TABLE  "+name+" (id, username, full_name, profile_pic_url, is_verified, followed_by_viewer, requested_by_viewer)")

    conn.commit()
    conn.close()

def create_table(db, tableName):
    conn = sqlite3.connect("C:/Users/Igor/Documents/Dev/projects/IGE/db/"+db+".db")
    print("Connected to "+db)
    c = conn.cursor()
    
    c.execute("CREATE TABLE  "+tableName+" (id, username, full_name, profile_pic_url, is_verified, followed_by_viewer, requested_by_viewer)")
    print("Created table "+tableName+" in "+db)
    conn.commit()
    conn.close()

def search(term, db='MAIN', tableName='following'):
    conn = sqlite3.connect("C:/Users/Igor/Documents/Dev/projects/IGE/db/"+db+".db")
    print("Connected to "+db)
    c = conn.cursor()
    
    c.execute("SELECT * FROM "+tableName+" WHERE (username LIKE '%"+term+"%') OR (full_name LIKE '%"+term+"%')")
    rows = c.fetchall()
    print("Found %d results" % len(rows))
    
    conn.commit()
    conn.close()

    return rows

def deleteItems(db,tableName,term):
    conn = sqlite3.connect("C:/Users/Igor/Documents/Dev/projects/IGE/db/"+db+".db")
    print("Connected to "+db)
    c = conn.cursor()

    c.execute("SELECT * FROM "+tableName+" WHERE (username LIKE '%"+term+"%') OR (full_name LIKE '%"+term+"%')")
    rows = c.fetchall()

    confirm = input("Delete %d items from %s, %s? (Y/N): " % (len(rows), db, tableName))
    if confirm == 'Y' or confirm == 'y':
        c.execute("DELETE FROM "+tableName+" WHERE (username LIKE '%"+term+"%') OR (full_name LIKE '%"+term+"%')")
        print("Deleted %d items." % len(rows))
    else:
        print("Items not deleted.")

    conn.commit()
    conn.close()

def moveItems(toDB, toTable, term, fromDB='MAIN', fromTable='following'):
    items = search(term, fromDB, fromTable)

    conn = sqlite3.connect("C:/Users/Igor/Documents/Dev/projects/IGE/db/"+toDB+".db")
    c = conn.cursor()

    for row in items:
        print("Inserting item: "+ row[1])
        c.execute("INSERT INTO "+toTable+" values(?,?,?,?,?,?,?)", row)

    print("Done copying %d items" % len(items))
    conn.commit()
    conn.close()

    deleteItems(fromDB, fromTable, term)
              

