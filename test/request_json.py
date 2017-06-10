# -*- coding: utf-8 -*-
import requests
import json
r = requests.get("http://localhost:8000/pedidos/")
for s in  r.json():
    fl = s.get('fl')
    data={"fl":fl}
    r = requests.post("http://localhost:8000/pedidos/servido/", data)
    print r
