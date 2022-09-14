ifeq ($(OS),Windows_NT)
	os_shell := powershell
	copy_lib := .\resources\scripts\copy.ps1
else
	os_shell := $(SHELL)
	copy_lib := resources/scripts/copy.sh
endif

# -----------------------------------------------------------------

install:
	poetry check
	poetry lock
	poetry update
	poetry install

test:
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

all:
	make build
	make copy
	make integration
	poetry run python -m pip install --upgrade pip
