.PHONY: fixtures clean mock_data

fixtures: clean
	mkdir fixtures
	python generate_fixtures.py > fixtures/latest_fixture.json

clean:
	rm -rf fixtures
