import psycopg2

class Connect_db:
    def __init__(self, name_db, user_db, password_db):
        self.name_db = name_db
        self.user_db = user_db
        self.password_db = password_db
        self.conn = psycopg2.connect(database=self.name_db, user=self.user_db, password=self.password_db)



    def delete_table(self):
        with self.conn.cursor() as cur:
            cur.execute("""DROP TABLE phone;
                           DROP TABLE client;""")

            self.conn.commit()



    def create_db(self):
        with self.conn.cursor() as cur:
            cur.execute("""CREATE TABLE client(id SERIAL PRIMARY KEY,
                                name VARCHAR(60) NOT NULL,
                                surname VARCHAR(60) NOT NULL,
                                email VARCHAR NOT NULL);""")

            cur.execute("""CREATE TABLE phone(id SERIAL PRIMARY KEY,
                                number VARCHAR(12),
                                client_id INTEGER NOT NULL,
                                FOREIGN KEY(client_id) REFERENCES client(id) ON DELETE CASCADE);""")

        self.conn.commit()


    def add_client(self, client_name:str, client_surname:str, client_email:str):
        with self.conn.cursor() as cur:
            cur.execute("INSERT INTO client(name, surname, email) VALUES(%s,%s,%s);",
                        (client_name, client_surname, client_email))

        self.conn.commit()


    def add_phone_number(self, client_id:int, phone_number:str):
        with self.conn.cursor() as cur:
            cur.execute("INSERT INTO phone(client_id, number) VALUES(%s,%s);",
                        (client_id, phone_number))

        self.conn.commit()


    def change_client(self, client_id:int, name:str, surname:str, email:str):
        with self.conn.cursor() as cur:
            cur.execute("""UPDATE client SET name = %s, surname = %s, email = %s
                         WHERE client.id = %s;""",
                        (name, surname, email, client_id))

        self.conn.commit()


    def del_phone(self,client_id:int, number_phone:str):
        with self.conn.cursor() as cur:
            cur.execute("""DELETE FROM phone WHERE client_id = %s AND number = %s;""",
                        (client_id, number_phone))

        self.conn.commit()


    def del_client(self, client_id:int):
        with self.conn.cursor() as cur:
            cur.execute("""DELETE FROM client WHERE client.id = %s;""",
                        (client_id,))

        self.conn.commit()

    def search_client(self, text:str):
        with self.conn.cursor() as cur:
            cur.execute("""SELECT name, surname,email,number 
            FROM client 
            JOIN phone ON client_id = client.id
            WHERE name = %s OR surname = %s OR email = %s
            OR %s = (SELECT number 
            FROM phone);""",
                        (text,text,text,text))
            print(cur.fetchall())



Methods = Connect_db('clients_db', 'postgres','postgres')
Methods.create_db()
Methods.add_client("Вася", "Пупкин", "12345asdfg")
Methods.add_phone_number(1,'12345')
Methods.change_client(2, 'Timofej', "Kukamrad", 'no_email')
Methods.del_phone(1,'12345')
Methods.del_client(1)
Methods.search_client('Timofej')

