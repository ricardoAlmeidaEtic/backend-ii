help: ## Show help
	# From https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'



up: ## Start the application
	docker-compose up -d

down: ## Stop the application
	docker-compose down

build: ## Build the application
	docker-compose build

logs: ## Show logs
	docker-compose logs -f

clean: ## Clean the application
	docker-compose down --volumes --remove-orphans

test: ## Run tests
	docker-compose run api pytest

lint: ## Run linter
	docker-compose run api ruff .
