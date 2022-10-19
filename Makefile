# ----------------------------------------------------------------
# helpers/openai-helper
# ----------------------------------------------------------------

ifeq ($(OS),Windows_NT)
    os_shell := powershell
	copy_setup := resources/scripts/copy_setup.ps1
else
    os_shell := $(SHELL)
	copy_setup := resources/scripts/copy_setup.sh
endif

copy:
	$(os_shell) $(copy_setup)

# ----------------------------------------------------------------

install:
	poetry check
	poetry lock
	poetry update
	poetry install

test:
# 	TODO: 20220929; lot of mypi errors; solve later
#	poetry run mypy openai_helper
	poetry run pytest --disable-pytest-warnings

build:
	make install
	make test
	poetry build

integration:
	poetry run python drivers/driver_openai_connector.py
	poetry run python drivers/driver_extract_output.py "This is a test"
	poetry run python drivers/driver_openai_custom_model.py
	poetry run python drivers/driver_openai_helper.py

linters:
	poetry run pre-commit run --all-files
	poetry run flakeheaven lint

freeze:
	poetry run pip freeze > requirements.txt
	poetry run python -m pip install --upgrade pip

all:
	make build
	make integration
	make linters
	make copy
	make freeze
