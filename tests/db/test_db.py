def test_ping_database(database):
    assert database.ping() is True
