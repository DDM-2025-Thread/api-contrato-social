VENV_UVICORN = venv/bin/uvicorn
VENV_PIP = venv/bin/pip
VENV_PYTHON = venv/bin/python

.PHONY: dev prod install check seed

seed:
	@echo "🌱 Executando script de seeding (verificando/criando super admin)..."
	@$(VENV_PYTHON) seed.py
dev: seed
	@echo "🚀 Iniciando servidor em modo de desenvolvimento..."
	@ENVIRONMENT=development $(VENV_UVICORN) app.main:app --reload --host 127.0.0.1 --port 8000
prod:
	@echo "🔒 Iniciando servidor em modo de produção..."
	@ENVIRONMENT=production $(VENV_UVICORN) app.main:app --host 0.0.0.0 --port 8000
install:
	@$(VENV_PIP) install -r requirements.txt
check:
	@echo "🐍 Verificando a versão do Python no venv..."
	@$(VENV_PYTHON) --version