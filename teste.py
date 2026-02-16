import requests

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzIiwiZXhwIjoxNzcxODU5Mzg4fQ.ImFxy2GyTrVWcB24Jg_FoTtY7lL5Ywjx9Ec8TRRssz8"
}

requisicao = requests.get(
    "http://127.0.0.1:8000/auth/refresh",
    headers=headers
)
print(requisicao.status_code)
print(requisicao.text)

print(requisicao)
print(requisicao.json())


##eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzIiwiZXhwIjoxNzcxODU5Mzg4fQ.ImFxy2GyTrVWcB24Jg_FoTtY7lL5Ywjx9Ec8TRRssz8