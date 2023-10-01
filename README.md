# Welcome to project-williamsville

```
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

also need to manually install and setup the pylint git hook if wished

```
python3 -m pip install git-pylint-commit-hook
```

Please do not put APIKey in code

```
oct2_api_analysis.py -a <apikey>
python oct2_financial_contagion.py
```

install mod_wsgi