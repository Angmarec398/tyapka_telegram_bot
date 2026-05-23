# tyapka-telegram-bot

Telegram-бот для проекта **Тяпка** — обрабатывает команды пользователей и проксирует
их в бэкенд через `/internal/telegram/*`.

## Команды

| Команда | Описание |
|---|---|
| `/start <token>` | Привязать Telegram к аккаунту |
| `/start` | Инструкция по подключению |
| `/status` | Статус привязки и настройки уведомлений |
| `/mute` | Приостановить уведомления |
| `/unmute` | Возобновить уведомления |
| `/unlink` | Отвязать аккаунт |
| `/help` | Список команд |

## Переменные окружения

Скопируйте `.env.example` → `.env` и заполните:

```
TELEGRAM_BOT_TOKEN=...        # токен от @BotFather
BACKEND_BASE_URL=...          # URL бэкенда, напр. https://api.example.com
INTERNAL_API_TOKEN=...        # тот же, что INTERNAL_API_TOKEN в бэкенде
LOG_LEVEL=INFO
USE_WEBHOOK=false
```

## Локальный запуск

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
python -m app.main
```

## Docker

```bash
docker compose up --build
```

## Интеграция с основным docker-compose

Добавьте в корневой `docker-compose.yml` основного проекта:

```yaml
  tyapka-bot:
    build: ./tyapka-telegram-bot
    env_file: tyapka-telegram-bot/.env
    depends_on: [backend]
    networks: [internal]
    restart: unless-stopped
```

В `.env` бота укажите `BACKEND_BASE_URL=http://backend:8000`.
