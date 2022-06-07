import sqlite3


class Sqlite:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()

    def create_user_table(self):
        self.cur.execute('Create table if not exists users('
                         'id integer PRIMARY KEY AUTOINCREMENT NOT NULL,'
                         'chat_id integer,'
                         'login varchar(255),'
                         'password varchar(255),'
                         'email varchar(255),'
                         'lang varchar(20) DEFAULT "ru" NOT NULL,'
                         'paid varchar(20) DEFAULT "false" NOT NULL'
                         ')')

    def create_row(self, chat_id):
        self.cur.execute(f"Insert into users(chat_id) values('{chat_id}')")
        self.conn.commit()

    def insert_user_info(self, login, password, email):
        self.cur.execute('Insert into users(login,password,email) values(?,?,?)', (login, password, email))
        self.conn.commit()

    def exists_user(self, chat_id):
        self.cur.execute(f"Select count(*) from users where chat_id='{chat_id}'")
        return self.cur.fetchone()[0] > 0

    def exists_user_login(self, chat_id):
        self.cur.execute(f"Select login from users where chat_id = '{chat_id}'")
        return self.cur.fetchone()[0] is not None

    def exists_user_password(self, chat_id):
        self.cur.execute(f"Select password from users where chat_id = '{chat_id}'")
        return self.cur.fetchone()[0] is not None

    def exists_user_email(self, chat_id):
        self.cur.execute(f"Select email from users where chat_id = '{chat_id}'")
        return self.cur.fetchone()[0] is not None

    def get_user(self, chat_id):
        self.cur.execute(f"Select * from users where chat_id = '{chat_id}'")
        return self.cur.fetchone()

    def update_language(self, chat_id, lang):
        self.cur.execute(f"Update users Set lang = '{lang}' where chat_id = '{chat_id}'")
        self.conn.commit()

    def update_login(self, chat_id, login):
        self.cur.execute(f"Update users Set login='{login}' where chat_id='{chat_id}'")
        self.conn.commit()

    def update_password(self, chat_id, password):
        self.cur.execute(f"Update users Set password='{password}' where chat_id='{chat_id}'")
        self.conn.commit()

    def update_email(self, chat_id, email):
        self.cur.execute(f"Update users Set email='{email}' where chat_id='{chat_id}'")
        self.conn.commit()

    def get_user_info(self, chat_id):
        self.cur.execute(f"Select login, password, email from users where chat_id='{chat_id}'")
        return self.cur.fetchone()

    def is_paid(self, chat_id):
        self.cur.execute(f"Select paid from users where chat_id='{chat_id}'")
        return self.cur.fetchone()[0] == 'true'

    def update_paid(self, chat_id, paid):
        self.cur.execute(f"Update users Set paid='{paid}' where chat_id='{chat_id}'")
        self.conn.commit()
