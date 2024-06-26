# Redes de Datos Trabajo Práctico Final

Redes de Datos - Tecnicatura Universitaria en Inteligencia Artificial

## Integrantes:
- Giuliano Crenna @giulicrenna
- Bruno Pace @bpace1

## Como correr el cliente y el servidor

En dos terminales distintas correr:

### Servidor

```bash
./run_server.sh
```

### Client

```bash
./run_client.sh
```

## Como Instalar dependencias y Setup del proyecto:

*Windows:*

```bash
python -m venv .venv

.venv/Scripts/activate

pip install -r requirements.txt

.venv/Scripts/deactivate

python -m venv .venv_client

.venv_client/Scripts/activate

pip install requests

.venv_client/Scripts/deactivate
```

*Linux:*

```bash
python3 -m venv .venv

source .venv/bin/activate

pip3 install -r requirements.txt

source .venv/bin/deactivate

python3 -m venv .venv_client

source .venv_client/bin/activate

pip3 install -r requirements.txt

source .venv_client/bin/deactivate
```

## Cómo correr de forma remota y acceder a la API

- Ingresar al archivo server.py y cambiar el host por la IP del servidor.
- Ingresar al archivo client.py y cambiar el host por la IP del servidor.