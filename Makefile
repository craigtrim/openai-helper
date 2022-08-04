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

# smoke test - involves live API calls and assumptions around Keys and Authentication
# that are not appropriate for platform-agnostic build tests
smoke:
	poetry run python tests/driver_extract_output.py "This is a test"
	poetry run python tests/driver_openai_connector.py
	poetry run python tests/driver_openai_helper.py
	poetry run python tests/driver_openai_custom_model.py

copy:
	$(os_shell) $(copy_lib)

all:
	make build
	make copy
	poetry run python -m pip install --upgrade pip
