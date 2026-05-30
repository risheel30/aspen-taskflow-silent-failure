def test_root_works(client):
    r = client.get("/")
    assert r.status_code == 200


def test_create_needs_auth(client):
    r = client.post("/jobs", json={"items": []})
    assert r.status_code == 401


def test_create_job(client, auth_risheel):
    r = client.post("/jobs", headers=auth_risheel, json={"items": [{"id": "a", "amount": 5}]})
    assert r.status_code == 200
    assert r.json()["status"] == "queued"


def test_create_sets_items(client, auth_risheel):
    r = client.post("/jobs", headers=auth_risheel, json={"items": [{"id": "a", "amount": 5}]})
    assert len(r.json()["items"]) == 1


def test_list_mine_empty(client, auth_vaibhav):
    r = client.get("/jobs", headers=auth_vaibhav)
    assert r.status_code == 200
    assert r.json() == []


def test_list_mine_after_create(client, auth_risheel):
    client.post("/jobs", headers=auth_risheel, json={"items": [{"id": "a", "amount": 5}]})
    r = client.get("/jobs", headers=auth_risheel)
    assert len(r.json()) == 1


def test_get_job_by_id(client, auth_risheel):
    c = client.post("/jobs", headers=auth_risheel, json={"items": [{"id": "a", "amount": 5}]})
    job_id = c.json()["id"]
    r = client.get(f"/jobs/{job_id}", headers=auth_risheel)
    assert r.status_code == 200
    assert r.json()["id"] == job_id


def test_get_unknown_job(client, auth_risheel):
    r = client.get("/jobs/job-9999", headers=auth_risheel)
    assert r.status_code == 404


def test_get_other_user_job(client, auth_risheel, auth_vaibhav):
    c = client.post("/jobs", headers=auth_risheel, json={"items": [{"id": "a", "amount": 5}]})
    job_id = c.json()["id"]
    r = client.get(f"/jobs/{job_id}", headers=auth_vaibhav)
    assert r.status_code == 404


def test_run_good_batch_done(client, auth_risheel):
    c = client.post("/jobs", headers=auth_risheel, json={"items": [{"id": "a", "amount": 5}, {"id": "b", "amount": 3}]})
    job_id = c.json()["id"]
    r = client.post(f"/jobs/{job_id}/run", headers=auth_risheel)
    assert r.status_code == 200
    assert r.json()["status"] == "done"


def test_run_good_batch_processed(client, auth_risheel):
    c = client.post("/jobs", headers=auth_risheel, json={"items": [{"id": "a", "amount": 5}, {"id": "b", "amount": 3}]})
    job_id = c.json()["id"]
    r = client.post(f"/jobs/{job_id}/run", headers=auth_risheel)
    assert r.json()["processed"] == 2


def test_run_good_batch_total(client, auth_risheel):
    c = client.post("/jobs", headers=auth_risheel, json={"items": [{"id": "a", "amount": 5}, {"id": "b", "amount": 3}]})
    job_id = c.json()["id"]
    r = client.post(f"/jobs/{job_id}/run", headers=auth_risheel)
    assert r.json()["total"] == 8


def test_cancel_responds(client, auth_risheel):
    c = client.post("/jobs", headers=auth_risheel, json={"items": [{"id": "a", "amount": 5}]})
    job_id = c.json()["id"]
    r = client.post(f"/jobs/{job_id}/cancel", headers=auth_risheel)
    assert r.status_code == 200


def test_manager_reads_member_job(client, auth_risheel, auth_priya):
    c = client.post("/jobs", headers=auth_risheel, json={"items": [{"id": "a", "amount": 5}]})
    job_id = c.json()["id"]
    r = client.get(f"/jobs/{job_id}", headers=auth_priya)
    assert r.status_code == 200
