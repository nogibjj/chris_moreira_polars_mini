install:
	pip install --upgrade pip && pip install -r requirements.txt

format:
	nbqa black *.ipynb &&\
	black *.py && black test_*.py

lint:
	ruff check test_*.py && ruff check *.py --fix
	nbqa ruff *.ipynb --fix

container-lint:
	docker run --rm -i hadolint/hadolint < Dockerfile

test:
	python -m pytest -vv --nbval -cov=mylib -cov=main *.py test_*.py *.ipynb

refactor: format lint

deploy:
	#deploy goes here

all: install lint test format deploy
