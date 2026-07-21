.PHONY: demo test security-scan smoke clean

demo:
	uvicorn app.main:app --host 127.0.0.1 --port 8017 --reload

test:
	python3 scripts/run_tests.py

security-scan:
	bash scripts/security_scan.sh

smoke:
	bash scripts/smoke_demo.sh

clean:
	rm -rf .pytest_cache __pycache__ app/__pycache__ operations_copilot/__pycache__ tests/__pycache__
