import json
import os
import sys
from urllib.request import Request, urlopen


BASE_URL = (
    sys.argv[1]
    if len(sys.argv) > 1
    else os.environ.get("BASE_URL", "http://127.0.0.1:5000")
)


def request_json(method, path, payload=None):
    data = None
    headers = {}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    request = Request(BASE_URL + path, data=data, headers=headers, method=method)
    with urlopen(request) as response:
        return response.status, json.loads(response.read().decode("utf-8"))


def show(label, status, data):
    print(f"{label}: {status} {json.dumps(data, sort_keys=True)}")


def main():
    status, users = request_json("GET", "/api/users")
    assert status == 200 and isinstance(users, list) and users
    show("GET all users", status, users)

    user_id = users[0]["user_id"]
    status, user = request_json("GET", f"/api/users/{user_id}")
    assert status == 200 and user["user_id"] == user_id
    show("GET one user", status, user)

    new_user = {
        "name": "Alice Khalil",
        "email": "alice.khalil@example.com",
        "phone": "76123456",
        "address": "Sidon",
        "country": "Lebanon",
    }
    status, added = request_json("POST", "/api/users/add", new_user)
    assert status == 200 and added["name"] == new_user["name"]
    show("POST add user", status, added)

    added_id = added["user_id"]
    status, added_from_database = request_json("GET", f"/api/users/{added_id}")
    assert status == 200 and added_from_database == added
    show("GET after add", status, added_from_database)

    updated_payload = {
        **added,
        "phone": "76987654",
        "address": "Jounieh",
    }
    status, updated = request_json("PUT", "/api/users/update", updated_payload)
    assert status == 200 and updated["address"] == "Jounieh"
    show("PUT update user", status, updated)

    status, updated_from_database = request_json("GET", f"/api/users/{added_id}")
    assert status == 200 and updated_from_database == updated
    show("GET after update", status, updated_from_database)

    status, deleted = request_json("DELETE", f"/api/users/delete/{added_id}")
    assert status == 200 and deleted["status"] == "User deleted successfully"
    show("DELETE user", status, deleted)

    status, deleted_lookup = request_json("GET", f"/api/users/{added_id}")
    assert status == 200 and deleted_lookup == {}
    show("GET deleted user", status, deleted_lookup)

    status, users_after_delete = request_json("GET", "/api/users")
    assert status == 200 and all(
        user["user_id"] != added_id for user in users_after_delete
    )
    show("GET after delete", status, users_after_delete)

    print("All API checks passed.")


if __name__ == "__main__":
    main()
