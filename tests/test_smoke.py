def test_root_works(client):
    r = client.get("/")
    assert r.status_code == 200


def test_create_needs_auth(client):
    r = client.post("/jobs", json={"kind": "export", "payload": {}})
    assert r.status_code == 401


def test_create_export_job(client, auth_risheel):
    r = client.post("/jobs", headers=auth_risheel, json={"kind": "export", "payload": {}})
    assert r.status_code == 200
    assert r.json()["status"] == "queued"


def test_create_invalid_kind(client, auth_risheel):
    r = client.post("/jobs", headers=auth_risheel, json={"kind": "banana", "payload": {}})
    assert r.status_code == 400


def test_list_mine_empty(client, auth_vaibhav):
    r = client.get("/jobs", headers=auth_vaibhav)
    assert r.status_code == 200
    assert r.json() == []


def test_list_mine_after_create(client, auth_risheel):
    client.post("/jobs", headers=auth_risheel, json={"kind": "export", "payload": {}})
    r = client.get("/jobs", headers=auth_risheel)
    assert len(r.json()) == 1


def test_get_job_by_id(client, auth_risheel):
    c = client.post("/jobs", headers=auth_risheel, json={"kind": "export", "payload": {}})
    job_id = c.json()["id"]
    r = client.get(f"/jobs/{job_id}", headers=auth_risheel)
    assert r.status_code == 200
    assert r.json()["id"] == job_id


def test_get_unknown_job(client, auth_risheel):
    r = client.get("/jobs/job-9999", headers=auth_risheel)
    assert r.status_code == 404


def test_get_other_user_job(client, auth_risheel, auth_vaibhav):
    c = client.post("/jobs", headers=auth_risheel, json={"kind": "export", "payload": {}})
    job_id = c.json()["id"]
    r = client.get(f"/jobs/{job_id}", headers=auth_vaibhav)
    assert r.status_code == 404


def test_run_export_succeeds(client, auth_risheel):
    c = client.post("/jobs", headers=auth_risheel, json={"kind": "export", "payload": {}})
    job_id = c.json()["id"]
    r = client.post(f"/jobs/{job_id}/run", headers=auth_risheel)
    assert r.status_code == 200
    assert r.json()["status"] == "succeeded"


def test_run_export_sets_result(client, auth_risheel):
    c = client.post("/jobs", headers=auth_risheel, json={"kind": "export", "payload": {}})
    job_id = c.json()["id"]
    r = client.post(f"/jobs/{job_id}/run", headers=auth_risheel)
    assert r.json()["result"]["ok"] is True


def test_cancel_responds(client, auth_risheel):
    c = client.post("/jobs", headers=auth_risheel, json={"kind": "export", "payload": {}})
    job_id = c.json()["id"]
    r = client.post(f"/jobs/{job_id}/cancel", headers=auth_risheel)
    assert r.status_code == 200


def test_create_two_within_quota(client, auth_manthan):
    a = client.post("/jobs", headers=auth_manthan, json={"kind": "export", "payload": {}})
    b = client.post("/jobs", headers=auth_manthan, json={"kind": "export", "payload": {}})
    assert a.status_code == 200
    assert b.status_code == 200


def test_manager_reads_member_job(client, auth_risheel, auth_priya):
    c = client.post("/jobs", headers=auth_risheel, json={"kind": "export", "payload": {}})
    job_id = c.json()["id"]
    r = client.get(f"/jobs/{job_id}", headers=auth_priya)
    assert r.status_code == 200
