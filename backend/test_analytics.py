import requests
token = requests.post("http://127.0.0.1:5000/auth/login", json={"email": "23f3001470@ds.study.iitm.ac.in", "password": "1234"}).json()["token"]
res = requests.get("http://127.0.0.1:5000/admin/analytics", headers={"Authorization": f"Bearer {token}"})
print(res.json())
