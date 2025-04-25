class UserRepository:
    def __init__(self, db_connector):
        self.db_connector = db_connector

    def get_by_id(self, user_id):
        with self.db_connector.connect().cursor(named_tuple=True) as cursor:
            cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            user = cursor.fetchone()
        return user

    def get_by_username_and_password(self, username, password):
        with self.db_connector.connect().cursor(named_tuple=True) as cursor:
            cursor.execute("SELECT * FROM users WHERE username = %s AND password_hash = %s", (username, password))
            user = cursor.fetchone()
        return user

    def all(self):
        with self.db_connector.connect().cursor(named_tuple=True) as cursor:
            cursor.execute("SELECT users.*, roles.name AS role FROM users LEFT JOIN roles")
            users = cursor.fetchall()
        return users
    
    def update(self, user_id, first_name, middle_name, last_name, role_id):
        connection = self.db_connector.connect()
        with connection.cursor(named_tuple=True) as cursor:
            query = ("UPDATE users SET first_name = %s, "
                    "middle_name = %s, last_name = %s, "
                    "role_id = %s WHERE id = %s")
            user_data = (first_name, middle_name, last_name, role_id, user_id)
            cursor.execute(query, user_data)
            connection.commit()

    def delete(self, user_id):
        connection = self.db_connector.connect()
        with connection.cursor(named_tuple=True) as cursor:
            cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
            connection.commit()