#!/usr/bin/env python
cd /home/ubuntu/samaritan-backend

python3 flaskapp/app.py &
python3 RecogScript.py

kill -- -$$
