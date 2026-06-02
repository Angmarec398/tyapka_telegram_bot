# tyapka-telegram-bot

Telegram-бот для проекта **Тяпка** — обрабатывает команды пользователей и проксирует
их в бэкенд через `/internal/telegram/*`.

## Команды

| Команда | Описание |
|---|---|
| `/start <token>` | Привязать Telegram к аккаунту |
| `/start` | Инструкция по подключению |
| `/status` | Статус привязки и настройки уведомлений |
| `/today` | Список дел на сегодняшний день |
| `/mute` | Приостановить уведомления |
| `/unmute` | Возобновить уведомления |
| `/unlink` | Отвязать аккаунт |
| `/help` | Список команд |

## Inline-навигация

Все команды кроме `/help` возвращают ответ с Inline-кнопками быстрого перехода:

| После команды | Кнопки |
|---|---|
| `/start` (привязка) | 📋 Статус · 🌱 Список дел |
| `/status` | 🌱 Список дел / 🔕 Приостановить / 🔓 Отвязать |
| `/today` | 📋 Статус |
| `/mute` (после выбора) | 📋 Статус · 🔔 Возобновить |
| `/unmute` | 📋 Статус · 🌱 Список дел |

## Переменные окружения

Скопируйте `.env.example` → `.env` и заполните:

```
TELEGRAM_BOT_TOKEN=...        # токен от @BotFather
TELEGRAM_BOT_USERNAME=...     # username бота без @
INTERNAL_API_TOKEN=...        # тот же, что INTERNAL_API_TOKEN в бэкенде
BACKEND_BASE_URL=...          # URL бэкенда, напр. http://172.19.0.2:8000
LOG_LEVEL=INFO                # уровень логирования (DEBUG/INFO/WARNING/ERROR)
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

Бот запускается в связке с WireGuard-контейнером для доступа к бэкенду через VPN.
Перед запуском убедитесь, что директория `wireguard/` содержит конфигурацию VPN.

## Деплой

CI/CD настроен через GitHub Actions (`.github/workflows/deploy.yml`).
При пуше в `master` автоматически:
1. Копирует файлы на сервер по SSH (rsync)
2. Записывает `.env` из GitHub Secrets
3. Пересобирает и перезапускает контейнеры
4. Ждёт статуса `healthy` от Docker healthcheck

Все секреты (`TELEGRAM_BOT_TOKEN`, `INTERNAL_API_TOKEN`, `BACKEND_BASE_URL` и др.)
хранятся в **Settings → Secrets and variables → Actions** репозитория.
