VENV_UVICORN = venv/bin/uvicorn
VENV_PIP = venv/bin/pip

.PHONY: dev prod install

dev:
	@echo "🚀 Iniciando servidor em modo de desenvolvimento..."
	@ENVIRONMENT=development $(VENV_UVICORN) app.main:app --reload --host 127.0.0.1 --port 8000
prod:
	@echo "🔒 Iniciando servidor em modo de produção..."
	@ENVIRONMENT=production $(VENV_UVICORN) app.main:app --host 0.0.0.0 --port 8000
install:
	@$(VENV_PIP) install -r requirements.txt