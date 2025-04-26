class UserRepository:
    def __init__(self, db_connector):
        self.db_connector = db_connector

    def get_by_id(self, user_id):
        with self.db_connector.connect().cursor(named_tuple=True) as cursor:
            cursor.execute("""
                SELECT users.*, roles.name as role_name 
                FROM users 
                LEFT JOIN roles ON users.role_id = roles.id 
                WHERE users.id = %s
            """, (user_id,))
            user = cursor.fetchone()
        return user

    def get_by_username(self, username):
        with self.db_connector.connect().cursor(named_tuple=True) as cursor:
            cursor.execute("""
                SELECT users.*, roles.name as role_name 
                FROM users 
                LEFT JOIN roles ON users.role_id = roles.id 
                WHERE users.username = %s
            """, (username,))
            user = cursor.fetchone()
        return user

    def get_by_username_and_password(self, username, password):
        with self.db_connector.connect().cursor(named_tuple=True) as cursor:
            cursor.execute("""
                SELECT users.*, roles.name as role_name 
                FROM users 
                LEFT JOIN roles ON users.role_id = roles.id 
                WHERE users.username = %s AND users.password_hash = %s
            """, (username, password))
            user = cursor.fetchone()
        return user

    def all(self):
        with self.db_connector.connect().cursor(named_tuple=True) as cursor:
            cursor.execute("""
                SELECT users.*, roles.name as role_name 
                FROM users 
                LEFT JOIN roles ON users.role_id = roles.id
            """)
            users = cursor.fetchall()
        return users
    
    def create(self, username, password_hash, first_name, last_name, middle_name=None, role_id=None):
        connection = self.db_connector.connect()
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO users (username, password_hash, first_name, last_name, middle_name, role_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (username, password_hash, first_name, last_name, middle_name, role_id))
            connection.commit()

    def update(self, user_id, first_name, last_name, middle_name=None, role_id=None):
        connection = self.db_connector.connect()
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE users 
                SET first_name = %s, last_name = %s, middle_name = %s, role_id = %s
                WHERE id = %s
            """, (first_name, last_name, middle_name, role_id, user_id))
            connection.commit()

    def update_password(self, user_id, password_hash):
        connection = self.db_connector.connect()
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE users 
                SET password_hash = %s
                WHERE id = %s
            """, (password_hash, user_id))
            connection.commit()

    def delete(self, user_id):
        connection = self.db_connector.connect()
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
            connection.commit()
            return cursor.rowcount > 0

    def get_all_roles(self):
        with self.db_connector.connect().cursor(named_tuple=True) as cursor:
            cursor.execute("SELECT id, name FROM roles")
            roles = cursor.fetchall()
            return [(role.id, role.name) for role in roles]