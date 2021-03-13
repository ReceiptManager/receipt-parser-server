.PHONY serve:

generate_cert:
	bash util/generate_certificate.sh

generate_token:
	bash util/generate_api_token.sh

serve:
	python src/receipt_server.py

PHONY: docker-build
docker-build:
	docker build -t monolidth/receipt-parser-server .

.PHONY: docker-push
docker-push:
	docker push monolidth/receipt-parser-server

.PHONY: docker-run
docker-run:
	docker run -v `pwd`/data/img:/app/data/img monolidth/receipt-parser-server
