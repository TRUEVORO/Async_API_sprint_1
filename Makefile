help: ## - Получить информацию о командах
	@sed \
		-e '/^[a-zA-Z0-9_\-]*:.*##/!d' \
		-e 's/:.*##\s*/:/' \
		-e 's/^\(.\+\):\(.*\)/$(shell tput setaf 6)\1$(shell tput sgr0):\2/' \
		$(MAKEFILE_LIST) | column -c2 -t -s :

run: ## - Запустить docker-compose
	docker-compose -f docker-compose.yaml up --build -d

down: ## - Уронить docker-compose
	docker-compose -f docker-compose.yaml down

clean: ## - Очистить docker
	docker stop $$(docker ps -aq)
	docker rm $$(docker ps -aq)
	docker rmi $$(docker images -q)
