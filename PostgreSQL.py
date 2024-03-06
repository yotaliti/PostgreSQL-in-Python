import psycopg2

conn = psycopg2.connect(database="homework5", user="postgres", password="Andrej10!")

with (conn.cursor() as cur):
    def create_table(cursor):
        cur.execute("""
        DROP TABLE phone_number;
        DROP TABLE clients;
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients(
            id      SERIAL PRIMARY KEY,
            name    VARCHAR(60) NOT NULL,
            surname VARCHAR(60) NOT NULL,
            email   VARCHAR(40) UNIQUE   
        );
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS phone_number(
            id          SERIAL PRIMARY KEY,
            client_id   INTEGER NOT NULL REFERENCES clients(id),
            number      VARCHAR(30)
        );
        """)

        conn.commit()


    create_table(cur)


    def insert_into_table(cursor, data):
        cursor.execute("""
        INSERT INTO clients
        VALUES (%s, %s, %s, %s);
        """, (data[0], data[1], data[2], data[3]))
        cursor.execute("""
        SELECT * FROM clients
        """)
        print(cursor.fetchall())


    def insert_phone_number(cursor, data):
        if len(data) == 5:
            cursor.execute("""
            INSERT INTO phone_number(client_id, number)
            VALUES (%s, %s);
            """, (data[0], data[4]))
        else:
            cursor.execute("""
            INSERT INTO phone_number(client_id, number)
            VALUES (%s, %s);
            """, (data[0], ' '))

        cursor.execute("""
        SELECT * FROM phone_number
        """)
        print(cursor.fetchall())


    def add_phone_number(cursor, id_client, new_number):
        cursor.execute("""
            SELECT number 
            FROM   phone_number
            WHERE  client_id = %s;
            """, (id_client,))
        if (new_number,) in cursor.fetchall():
            print('Такой номер клиента уже есть')
        else:
            cursor.execute("""
                INSERT INTO phone_number(client_id, number)
                VALUES (%s, %s)
                """, (id_client, new_number))
            cursor.execute("""
                SELECT * FROM phone_number;
                """)
            print(cursor.fetchall())


    def change_data(cursor, id_client, new_data):
        cursor.execute("""
        UPDATE clients
        SET    name = %s, surname = %s, email = %s
        WHERE  id = %s;
        """, (new_data[0], new_data[1], new_data[2], id_client))
        if len(new_data) == 4:
            cursor.execute("""
            DELETE FROM phone_number
            WHERE client_id = %s;
            """, (id_client,))
            cursor.execute("""
            INSERT INTO phone_number(client_id, number)
            VALUES (%s, %s)
            """, (id_client, new_data[3]))
        cursor.execute("""
        SELECT * FROM clients;
        """)
        print(cursor.fetchall())
        cursor.execute("""
        SELECT * FROM phone_number;
        """)
        print(cursor.fetchall())


    def del_phone_number(cursor, id_client, number):
        cursor.execute("""
        DELETE FROM phone_number
        WHERE client_id = %s
        AND number = %s;
        """, (id_client, number))
        cursor.execute("""
        SELECT * FROM phone_number;
        """)
        print(cursor.fetchall())


    def del_phone_number2(cursor, data_client):
        cursor.execute("""
        DELETE FROM phone_number
        WHERE client_id = (
        SELECT id FROM clients 
        WHERE name = %s AND surname = %s AND email = %s
        )
        """, (data_client[0], data_client[1], data_client[2]))
        cursor.execute("""
        SELECT * FROM phone_number
        """)
        print(cursor.fetchall())


    def del_client(cursor, id_client):
        cursor.execute("""
        DELETE FROM phone_number
        WHERE client_id = %s
        """, (id_client,))
        cursor.execute("""
        DELETE FROM clients
        WHERE id = %s
        """, (id_client,))
        cursor.execute("""
        SELECT * FROM clients;
        """)
        print(cursor.fetchall())
        cursor.execute("""
        SELECT * FROM phone_number;
        """)
        print(cursor.fetchall())


    def find_client(cursor, query):
        cursor.execute("""
        SELECT name, surname, email, number FROM clients c
        JOIN   phone_number ph ON ph.client_id = c.id
        WHERE  name = %s OR surname = %s OR email = %s OR number = %s
        """, (query, query, query, query))
        print(cursor.fetchall())


    me = (1, 'Andrej', 'Lytaev', 'man@gmail.com')
    she = (2, 'Sara', 'Parker', 'woman@gmail.com', '89824748490')

    insert_into_table(cur, me)
    insert_phone_number(cur, me)

    insert_into_table(cur, she)
    insert_phone_number(cur, she)

    add_phone_number(cur, 1, '888888888888')
    add_phone_number(cur, 2, '111111111111')

    she_wife = ('Sara', 'Lytaeva', 'wife@gmail.com', '222222222222')
    change_data(cur, 2, she_wife)

    add_phone_number(cur, 2, '111111111111')
    del_phone_number(cur, 2, '222222222222')
    add_phone_number(cur, 2, '111111111111')

    client1 = ('Sara', 'Lytaeva', 'wife@gmail.com')
    client2 = ('Piter', 'Lytaev', 'trewq@mail.ru')
    del_phone_number2(cur, client1)
    del_phone_number2(cur, client2)

    add_phone_number(cur, 2, '111111111111')

    son = (3, 'John', 'Lytaev', 'son@gmail.com')

    insert_into_table(cur, son)
    insert_phone_number(cur, son)

    del_client(cur, 2)

    find_client(cur, 'John')
    find_client(cur, '888888888888')
    find_client(cur, 'qwerty@mail.ru')

conn.close()
