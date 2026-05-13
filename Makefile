GREEN = \033[0;32m
YELLOW = \033[0;33m
RESET = \033[0m

VENV = .venv
PY = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip
POETRY = $(PY) -m poetry

MAIN = a_maze_ing.py
CONFIG = config.txt
ARGS ?= $(CONFIG)

all: run

$(VENV):
	@echo "$(GREEN)[LOG] Criando ambiente virtual... $(RESET)"
	@python3 -m venv $(VENV)
	@$(PIP) install --upgrade pip

install: $(VENV)
	@echo "$(GREEN)[LOG] Instalando dependências do projeto...$(RESET)"
	@$(PIP) install flake8 mypy poetry

run: install
	@echo "$(GREEN)[LOG] Executando o gerador de labirintos... $(RESET)"
	@echo "$(YELLOW)[INFO] Arquivo utilizado: $(ARGS)$(RESET)"
	@$(PY) $(MAIN) $(ARGS)

build: install
	@echo "$(GREEN)[LOG] Gerando pacote (.whl) com Poetry...$(RESET)"
	@$(POETRY) build
	@cp dist/mazegen-*.whl .
	@echo "$(YELLOW)[INFO] Pacote copiado para a raiz.$(RESET)"

debug: install
	@echo "$(GREEN)[LOG] Iniciando depurador com $(ARGS)... $(RESET)"
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

reqs: install
	@echo "$(YELLOW)[INFO] Exportando dependências para requirements.txt...$(RESET)"
	@$(POETRY) export -f requirements.txt --output requirements.txt --without-hashes

clean:
	@echo "$(GREEN)[LOG] Removendo caches temporários...$(RESET)"
	@rm -rf .mypy_cache .pytest_cache
	@find . -type d -name "__pycache__" -exec rm -rf {} +

fclean: clean
	@echo "$(GREEN)[LOG] Removendo ambiente virtual... $(RESET)"
	@rm -rf $(VENV)

re: fclean all

.PHONY: all install run debug lint lint-strict reqs clean fclean re
