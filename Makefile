GREEN = \033[0;32m
YELLOW = \033[0;33m
RESET = \033[0m

VENV = .venv
PY = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

MAIN = a_maze_ing.py

all: install

$(VENV):
	@echo "$(GREEN)[LOG] Criando ambiente virtual... $(RESET)"
	@python3 -m venv $(VENV)
	@$(PIP) install --upgrade pip

install: $(VENV)
	@echo "$(GREEN)[LOG] Instalando dependências do projeto...$(RESET)"
	@$(PIP) install flake8 mypy poetry

run: install
	@echo "$(GREEN)[LOG] Executando o gerador de labirintos... $(RESET)"
	@$(PY) $(MAIN) $(ARGS)
	@if [ ! -z "$(ARGS)" ]; then \
		echo "$(YELLOW)[INFO] Argumentos passados: $(ARGS)$(RESET)"; \
	else \
		echo "$(YELLOW)[INFO] Nenhum argumento passado.$(RESET)"; \
	fi

debug: install
	@echo "$(GREEN)[LOG] Iniciando depurador... $(RESET)"
	@$(PY) -m pdb $(MAIN) $(ARGS)

lint: install
	@echo "$(GREEN)[LOG] Verificando estilo com Flake8...$(RESET)"
	@$(PY) -m flake8 .
	@echo "$(GREEN)[LOG] Verificando tipos com MyPy...$(RESET)"
	@$(PY) -m mypy --warn-return-any --warn-unused-ignores --ignore-missing-imports \
		--disallow-untyped-defs --check-untyped-defs .

lint-strict: install
	@echo "$(GREEN)[LOG] Rodando MyPy em modo STRICT...$(RESET)"
	@$(PY) -m mypy --strict .

reqs:
	@echo "$(YELLOW)[INFO] Exportando dependências para requirements.txt...$(RESET)"
	@$(PY) -m poetry export -f requirements.txt --output requirements.txt --without-hashes

clean:
	@echo "$(GREEN)[LOG] Removendo caches temporários...$(RESET)"
	@rm -rf .mypy_cache .pytest_cache
	@find . -type d -name "__pycache__" -exec rm -rf {} +

fclean: clean
	@echo "$(GREEN)[LOG] Removendo ambiente virtual... $(RESET)"
	@rm -rf $(VENV)

re: fclean all

.PHONY: all install run debug lint lint-strict reqs clean fclean re
