# FastAPI Movie Catalog

## Develop

### Setup

Right click: `movie-catalog` -> Mar directory as -> Sources root

### Configure pre-commit

Install pre-commit hook:
```shell
pre-commit install
```

### Install

Install packages:
```shell
uv sync
````

### Run

Go to workdir:
```shell
cd movie-catalog
```

Run dev server:
```shell
fastapi dev
```

## Snippets

```shell
python3 -c "import secrets;print(secrets.token_urlsafe(16))"
```
