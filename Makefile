# make help - find available targes in the Makefile
.PHONY: help
help:
	@echo " pre-commit           Run pre-commit hooks"
	@echo " run-tests            Run tests"
	@echo " run-me           	 Run the project"

# make pre-commit - run pre-commit hooks
.PHONY: pre-commit
pre-commit:
	poetry run pre-commit run --all-files

# make run-tests - run tests
.PHONY: run-tests
run-tests: rebuild-system
	poetry run pytest
	$(MAKE) kill-system

.PHONY: start-database
start-database:
	docker compose up -d db

.PHONY: stop-database
stop-database:
	docker compose stop db

.PHONY: kill-system
kill-system:
	docker compose down --volumes --remove-orphans


.PHONY: rebuild-system
rebuild-system: kill-system
	docker compose build --no-cache
	docker compose up -d
	poetry run alembic upgrade head
	poetry run python tests/populate.py

.PHONY: run-me
run-me: rebuild-system
	poetry run python -m main
	$(MAKE) kill-system
