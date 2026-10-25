# Интернет-магазин одежды

Микросервисный интернет-магазин: каталог товаров, поиск, корзина, оформление заказов и админ-панель.

## Стек

- **Backend:** Python 3.13, FastAPI, SQLAlchemy, SQLite
- **Авторизация:** JWT (Ed25519), refresh-токены в httpOnly cookie с ротацией, пароли — Argon2
- **Frontend:** React 19, React Router, Vite
- **Инфраструктура:** Docker, Docker Compose

## Архитектура

| Сервис     | Порт | Назначение                                                        |
|------------|------|-------------------------------------------------------------------|
| `frontend` | 5173 | SPA на React, запускается через Vite                              |
| `gateway`  | 8000 | Единая точка входа: проверяет access-токен и проксирует запросы   |
| `auth`     | 8002 | Регистрация, вход, выпуск и обновление токенов                    |
| `core`     | 8001 | Товары, корзина, заказы, статика с изображениями                  |

Наружу открыты только `frontend` и `gateway`, сервисы `auth` и `core` доступны лишь внутри docker-сети.
`auth` подписывает токены приватным ключом, `gateway` и `core` проверяют их публичным.

## Запуск

Нужен установленный [Docker](https://docs.docker.com/get-docker/) с Docker Compose.

```bash
git clone https://github.com/lo2s452/Koi-Market.git
cd Koi-Market
docker compose up --build
```

После сборки открыть **http://localhost:5173**.

В базе уже есть 16 товаров с изображениями. Ключи и настройки лежат в репозитории, дополнительно ничего настраивать не нужно.

### Администратор

Для доступа к админ-панели (добавление товаров, управление заказами) создайте администратора:

```bash
docker compose exec auth python -m app.cli create-admin admin
```

Команда попросит ввести пароль дважды.

### Полезные команды

```bash
docker compose up --build -d   # запуск в фоне
docker compose logs -f         # логи всех сервисов
docker compose down            # остановка и удаление контейнеров, базы вернутся к исходному состоянию
```

## Запуск без Docker

Каждый backend-сервис запускается из своей папки:

```bash
cd auth      # или core, gateway
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --port 8002   # core — 8001, gateway — 8000
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```
