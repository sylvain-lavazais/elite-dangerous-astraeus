PWD=$(shell pwd)
.DEFAULT_GOAL := help

##  -------
##@ Install
##  -------

install: .nx-install ## Install locally the application
	@echo "===> $@ <==="
	@nx run-many -t install
.PHONY: install

build: .nx-install ## Build the application
	@echo "===> $@ <==="
	@nx run-many -t build
.PHONY: build

##  -------
##@ Quality
##  -------

test: .nx-install ## Run all tests
	@echo "===> $@ <==="
	@nx run-many -t test --parallel=5
.PHONY: test

lint: .nx-install ## Run all linter
	@echo "===> $@ <==="
	@nx run-many -t lint --parallel=5
.PHONY: lint

##  ----
##@ Run
##  ----

run: ## Run locally the application
	@echo "===> $@ <==="
	@python -m eddn-
.PHONY: run

##  ----
##@ Misc
##  ----

.nx-install:
	@echo "===> $@ <==="
	@echo "Node version:"
	@if ! node --version ; then echo "Node not installed /!\\"; fi
	@if ! nx --version ; then npm i -g nx; fi
.PHONY: .nx-install

.DEFAULT_GOAL := help
APPLICATION_TITLE := Astraeus \n ========
.PHONY: help
# See https://www.thapaliya.com/en/writings/well-documented-makefiles/
help: ## Display this help
	@awk 'BEGIN {FS = ":.* ##"; printf "\n\033[32;1m ${APPLICATION_TITLE}\033[0m\n\n\033[1mUsage:\033[0m\n  \033[31mmake \033[36m<option>\033[0m\n"} /^[%a-zA-Z_-]+:.* ## / { printf "  \033[33m%-25s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' ${MAKEFILE_LIST}

##@
