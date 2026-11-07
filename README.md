# Web Enumeration CTF

## Run With Python

```powershell
pip install -r requirements.txt
python app.py
```

The app listens on:

```text
http://0.0.0.0:5000
```

From the same machine, open:

```text
http://127.0.0.1:5000/
```

## Run With Flask

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:FLASK_APP = "app.py"
flask run --host=0.0.0.0 --port=5000
```

## Run With Waitress

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
waitress-serve --host=0.0.0.0 --port=5000 wsgi:app
```

## Run In Docker

Build and run locally, then open <http://127.0.0.1:5000/>:

```powershell
docker build -t web-enum .
docker run --rm -p 127.0.0.1:5000:5000 web-enum
```

This intentionally vulnerable challenge must only run on an isolated CTF
challenge runner. Do not expose it directly as a public service.
