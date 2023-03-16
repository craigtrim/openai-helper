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
	poetry run pytest --disable-pytest-warnings

build:
	make install
	make test
	poetry build

integration:
	poetry run python drivers/extract_primary_topic_driver.py
	poetry run python drivers/output_extractor_text_driver.py
	poetry run python drivers/output_extractor_text_plac.py "This is a test"
	poetry run python drivers/openai_connector_driver.py
#	poetry run python drivers/openai_custom_model_driver.py
	poetry run python drivers/openai_helper_driver.py
	poetry run python drivers/run_chat_completion_driver.py

linters:
	poetry run pre-commit run --all-files
	poetry run flakeheaven lint

freeze:
	poetry run pip freeze > requirements.txt
	poetry run python -m pip install --upgrade pip

all:
	make linters
	make build
	make integration
	make copy
	make freeze

fast:
	make install
	poetry build
