# udacity-devops-capstone

```
  _________________________________________________
 /                                                 \
| Udacity AWS DevOps capstone project bringing      |
| cowsays to the web                                |
 \                                                 /
  =================================================
                                                      \
                                                       \
                                                         ^__^
                                                         (oo)\_______
                                                         (__)\       )\/\
                                                             ||----w |
                                                             ||     ||
```

# service API

... just as a bunch of curl calls...

## service version

```
curl -X GET http://127.0.0.1:8080/
```

## available speakers

```
curl -X GET http://127.0.0.1:8080/speakers
```

## say something as...

```
curl -X POST -F 'speaker=stimpy' -F 'message=Blargh!' http://127.0.0.1:8080/say
```

# development

## setup

Requires python >= 3.6.

```
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

## liniting / testing

Run the linter:

```
pylint *.py
```

Run basic smoke test:
```
python smoke_test.py
```

**Note:** smoke tests accepts the target address (<host>:<port>) as env var _COWSAY_SERVICE_ADDRESS_