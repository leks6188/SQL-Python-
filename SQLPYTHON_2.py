import psycopg2

with psycopg2.connect(database="clients_db", user="postgres", password="postgres") as conn:

    def delete_table():
        with conn.cursor() as cur:
            cur.execute("""DROP TABLE phone;
                            DROP TABLE client;""")
        conn.commit()

    def create_db():
        with conn.cursor() as cur:
            cur.execute("""CREATE TABLE client(id SERIAL PRIMARY KEY,
                                name VARCHAR(60) NOT NULL,
                                surname VARCHAR(60) NOT NULL,
                                email VARCHAR NOT NULL);""")

            cur.execute("""CREATE TABLE phone(id SERIAL PRIMARY KEY,
                                number VARCHAR(12),
                                client_id INTEGER NOT NULL,
                                FOREIGN KEY(client_id) REFERENCES client(id) ON DELETE CASCADE);""")
        conn.commit()


    def add_client(client_name:str, client_surname:str, client_email:str):
        with conn.cursor() as cur:
            cur.execute("INSERT INTO client(name, surname, email) VALUES(%s,%s,%s);",
                        (client_name, client_surname, client_email))
        conn.commit()


    def add_phone_number(client_id:int, phone_number:str):
        with conn.cursor() as cur:
            cur.execute("INSERT INTO phone(client_id, number) VALUES(%s,%s);",
                        (client_id, phone_number))
        conn.commit()


    def change_client(client_id:int, name:str = None, surname:str = None, email:str = None):
        with conn.cursor() as cur:
            query = []
            vars = []

            if name != None:
                query += ['name = %s']
                vars += [name]

            if surname != None:
                query += ['surname = %s']
                vars += [surname]

            if email != None:
                query += ['email = %s']
                vars += [email]
            vars += [client_id]

            cur.execute(query = "UPDATE client SET " + ','.join(query) + ' WHERE client.id = %s;',
                        vars = vars)
        conn.commit()


    def del_phone(client_id:int, number_phone:str):
        with conn.cursor() as cur:
            cur.execute("""DELETE FROM phone WHERE client_id = %s AND number = %s;""",
                        (client_id, number_phone))
        conn.commit()


    def del_client(client_id:int):
        with conn.cursor() as cur:
            cur.execute("""DELETE FROM client WHERE client.id = %s;""",
                        (client_id,))
        conn.commit()


    def search_client(name=None, surname=None, email=None, number=None):
        with conn.cursor() as cur:
            query = []
            vars = []

            if name != None:
                query += ['name = %s']
                vars += [name]

            if surname != None:
                query += ['surname = %s']
                vars += [surname]

            if email != None:
                query += ['email = %s']
                vars += [email]

            if number != None:
                query += ['number = %s']
                vars += [number]

            cur.execute(query = """SELECT name, surname, email, number
                FROM client 
                LEFT JOIN phone ON client_id = client.id
                WHERE """ + ' AND '.join(query),
                        vars = vars)
            print(cur.fetchall())



if __name__ == '__main__':
    #delete_table()
    #create_db()
    #add_client("James", "Kuk", "54321")
    #add_phone_number(1,'1111111')
    #change_client(2,'Fernan','Magellan','Trinidad')
    #del_phone(1,'1111111')
    #del_client(1)
    #search_client("Fernan")

conn.close()