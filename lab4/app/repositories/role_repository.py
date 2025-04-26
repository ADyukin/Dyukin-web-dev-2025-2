class RoleRepository:
    def __init__(self, db_connector):
        self.db_connector = db_connector

    def get_by_id(self, role_id):
        with self.db_connector.connect().cursor(named_tuple=True) as cursor:
            cursor.execute("""
                SELECT * FROM roles WHERE id = %s
            """, (role_id,))
            role = cursor.fetchone()
        return role

    def get_by_name(self, name):
        with self.db_connector.connect().cursor(named_tuple=True) as cursor:
            cursor.execute("""
                SELECT * FROM roles WHERE name = %s
            """, (name,))
            role = cursor.fetchone()
        return role

    def all(self):
        with self.db_connector.connect().cursor(named_tuple=True) as cursor:
            cursor.execute("SELECT * FROM roles")
            roles = cursor.fetchall()
        return roles

    def create(self, name, description=None):
        connection = self.db_connector.connect()
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO roles (name, description)
                VALUES (%s, %s)
            """, (name, description))
            connection.commit()

    def update(self, role_id, name, description=None):
        connection = self.db_connector.connect()
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE roles 
                SET name = %s, description = %s
                WHERE id = %s
            """, (name, description, role_id))
            connection.commit()

    def delete(self, role_id):
        connection = self.db_connector.connect()
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM roles WHERE id = %s", (role_id,))
            connection.commit()
            return cursor.rowcount > 0
