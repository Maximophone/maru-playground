install:
	poetry install

run:
	cd maru_playground && poetry run flask run --host=0.0.0.0