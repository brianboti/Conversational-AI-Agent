from callbot import create_app

def test_health_root():
    app = create_app()
    c = app.test_client()
    r = c.get("/")
    assert r.status_code == 200
    assert r.data == b"OK"
