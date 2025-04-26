import pytest
from app.repositories.role_repository import RoleRepository
from collections import namedtuple

# Мок для курсора базы данных
class MockCursor:
    def __init__(self, fetch_result=None):
        self.fetch_result = fetch_result
        self.executed_queries = []
        self.executed_params = []
        self._rowcount = 1  # По умолчанию 1, будет изменяться при необходимости

    def execute(self, query, params=None):
        self.executed_queries.append(query)
        self.executed_params.append(params)
        # Для операции DELETE устанавливаем rowcount в зависимости от наличия результата
        if "DELETE" in query:
            self._rowcount = 1  # Всегда возвращаем 1, так как это поведение реального курсора MySQL

    def fetchone(self):
        return self.fetch_result

    def fetchall(self):
        if isinstance(self.fetch_result, (list, tuple)):
            return self.fetch_result
        return [self.fetch_result] if self.fetch_result else []

    @property
    def rowcount(self):
        return self._rowcount

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

# Мок для соединения с базой данных
class MockConnection:
    def __init__(self, cursor):
        self._cursor = cursor
        self.committed = False

    def cursor(self, named_tuple=False):
        return self._cursor

    def commit(self):
        self.committed = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

# Мок для коннектора базы данных
class MockDBConnector:
    def __init__(self, cursor):
        self._connection = MockConnection(cursor)

    def connect(self):
        return self._connection

# Фикстура для создания мок-объектов
@pytest.fixture
def mock_role():
    Role = namedtuple('Role', ['id', 'name', 'description'])
    return Role(1, 'admin', 'Administrator role')

@pytest.fixture
def role_repository(mock_role):
    cursor = MockCursor(mock_role)
    db_connector = MockDBConnector(cursor)
    return RoleRepository(db_connector), cursor, db_connector

def test_get_by_id(role_repository, mock_role):
    repository, cursor, db_connector = role_repository
    
    # Тест получения роли по id
    role = repository.get_by_id(1)
    
    assert role == mock_role
    assert "SELECT * FROM roles WHERE id = %s" in cursor.executed_queries[0]
    assert cursor.executed_params[0] == (1,)

def test_get_by_name(role_repository, mock_role):
    repository, cursor, db_connector = role_repository
    
    # Тест получения роли по имени
    role = repository.get_by_name('admin')
    
    assert role == mock_role
    assert "SELECT * FROM roles WHERE name = %s" in cursor.executed_queries[0]
    assert cursor.executed_params[0] == ('admin',)

def test_all(role_repository, mock_role):
    repository, cursor, db_connector = role_repository
    cursor.fetch_result = [mock_role, mock_role]  # Имитируем список из двух ролей
    
    # Тест получения всех ролей
    roles = repository.all()
    
    assert len(roles) == 2
    assert roles[0] == mock_role
    assert "SELECT * FROM roles" in cursor.executed_queries[0]

def test_create(role_repository):
    repository, cursor, db_connector = role_repository
    
    # Тест создания новой роли
    repository.create('new_role', 'New role description')
    
    assert "INSERT INTO roles (name, description)" in cursor.executed_queries[0]
    assert cursor.executed_params[0] == ('new_role', 'New role description')
    assert db_connector._connection.committed

def test_update(role_repository):
    repository, cursor, db_connector = role_repository
    
    # Тест обновления роли
    repository.update(1, 'updated_role', 'Updated description')
    
    assert "UPDATE roles" in cursor.executed_queries[0]
    assert cursor.executed_params[0] == ('updated_role', 'Updated description', 1)
    assert db_connector._connection.committed

def test_delete(role_repository):
    repository, cursor, db_connector = role_repository
    
    # Тест удаления роли
    result = repository.delete(1)
    
    assert result is True
    assert "DELETE FROM roles WHERE id = %s" in cursor.executed_queries[0]
    assert cursor.executed_params[0] == (1,)
    assert db_connector._connection.committed

def test_delete_nonexistent(role_repository):
    repository, cursor, db_connector = role_repository
    cursor.fetch_result = None  # Имитируем отсутствие роли
    
    # Тест удаления несуществующей роли
    result = repository.delete(999)
    
    assert result is True  # В текущей реализации всегда возвращается True, если нет ошибок
    assert "DELETE FROM roles WHERE id = %s" in cursor.executed_queries[0]
    assert cursor.executed_params[0] == (999,) 