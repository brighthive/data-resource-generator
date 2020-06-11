def test_ping_database(database):
    assert database.ping() == True
