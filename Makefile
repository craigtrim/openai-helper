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
	poetry run python tests/test_openai_connector_creds.py
	poetry run python tests/test_openai_helper_creds.py

copy:
	$(os_shell) $(copy_lib)

all:
	make build
	make copy
	poetry run python -m pip install --upgrade pip
