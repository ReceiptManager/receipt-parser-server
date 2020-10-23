clean:
	rm -r data/img/*
	rm -r data/tmp/*
	rm -r data/out/*

generate_cert:
	bash util/generate_certificate.sh

serve:
	python src/main/server.py
