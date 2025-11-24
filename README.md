# Orders API

API REST para gerenciamento de fila de pedidos usando Flask.

## Instalação

### Opção 1: Usando o script de setup (Recomendado)

```bash

python3 scripts/setup_env.py

pip install -e .
setup-env
```

### Opção 2: Instalação manual

```bash

python3 -m venv .venv

source .venv/bin/activate  #LINUX

.venv\Scripts\activate  #W11

pip install -e .
```

## Execução

```bash
python api/app.py
```

API disponível em `http://localhost:1607`

## Testes

### Opção 1: Usando o script de testes

```bash
run-tests

python3 scripts/run_tests.py

pytest tests/testE2E/test_e2e.py -v
```


## Endpoints

- `POST /order/put` - Cria um novo pedido
- `GET /order/get` - Obtém o próximo pedido da fila
- `POST /order/finish` - Marca um pedido como finalizado
- `POST /order/cancel` - Cancela um pedido
- `GET /order/cancel_by_id?id=X` - Cancela um pedido por ID
- `GET /order/status?id=X` - Obtém status de um pedido
