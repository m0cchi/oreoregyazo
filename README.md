# OREOREGYAZO
## setup client
1. get GyazoClient
2. modify HOST and PORT (optional http.use_ssl)
```bash
cp -r /Applications/Gyazo.app /Applications/GyazoAlt.app
EDITOR=emacs $EDITOR /Applications/GyazoAlt.app/Contents/Resources/script
```

## startup server
```bash
pipenv run python app.py
```
