.PHONY: run development containers
dev:
	docker compose -f compose.dev.yaml up

.PHONY: run production containers
prod:
	docker compose -f compose.prod.yaml up -d

.PHONY: build server container
build:
	(cd src && docker build -t crosspost .)
