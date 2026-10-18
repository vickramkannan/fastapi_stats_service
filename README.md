# FastAPI Descriptive Statistics Service

## Deploy on Render
1. Upload these files to a GitHub repository.
2. In Render, choose **New + → Blueprint** and connect the repository (or create a Web Service with the commands below).
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Set environment variable `USER_EMAIL` to your exact logged-in email: `22f3000616@ds.study.iitm.ac.in`.
6. Deploy and copy the public `https://....onrender.com` base URL into the grader.

## Local test
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Test stats:
```bash
curl 'http://127.0.0.1:8000/stats?values=1,2,3'
```

Test allowed-origin preflight:
```bash
curl -i -X OPTIONS 'http://127.0.0.1:8000/stats' \
  -H 'Origin: https://dash-8yzo4n.example.com' \
  -H 'Access-Control-Request-Method: GET'
```

Test rejected-origin preflight:
```bash
curl -i -X OPTIONS 'http://127.0.0.1:8000/stats' \
  -H 'Origin: https://evil.example' \
  -H 'Access-Control-Request-Method: GET'
```

Only the assigned origin receives `Access-Control-Allow-Origin`. The middleware adds `X-Request-ID` and `X-Process-Time` to all HTTP responses.
