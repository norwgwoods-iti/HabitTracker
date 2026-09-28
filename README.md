# 🌿 Habit Tracker

Учебный проект для ресурса Solvate - [solvit.space/projects/habit_tracker](https://solvit.space)

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/SQLAlchemy-2.0-CC292B?style=for-the-badge&logo=sqlalchemy&logoColor=white" alt="SQLAlchemy">
  <img src="https://img.shields.io/badge/JavaScript-Vanilla-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" alt="JS">
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="HTML5">
</p>


> **Habit Tracker** — это легкое, современное асинхронное веб-приложение для отслеживания ежедневных привычек. Проект реализован с использованием классической архитектуры: **FastAPI REST API** на бэкенде и динамический **Single Page Application (SPA)** фронтенд в едином HTML-файле.

---

## 🛠 Технологический стек

### **Backend**
* **Python 3.12**
* **FastAPI** — асинхронный фреймворк для быстрого создания RESTful API
* **SQLAlchemy 2.0 (AsyncIO)** — ORM для работы с базой данных
* **APScheduler** — фоновый планировщик задач (автоматически обновляет статусы привычек каждую ночь в 00:00)
* **Pydantic v2** — валидация данных и сериализация
* **Uvicorn** — асинхронный ASGI-сервер
* **Docker** — контейнеризация приложения

### **Frontend**
* **Vanilla JavaScript (ES6+)** — отправка асинхронных запросов через `fetch`
* **CSS3 & Flexbox/Grid** — адаптивная верстка
* **FontAwesome 6** — векторная иконографика

---

## ⚙️ Способы запуска проекта

Вы можете запустить проект двумя способами: быстро через **Docker** (рекомендуется, не требует настройки окружения) или **локально** в виртуальном окружении.

### Вариант 1: Запуск через Docker (Быстрый старт) 🐳

Убедитесь, что у вас установлен и запущен [Docker Desktop](https://docker.com).

```bash
# 1. Клонируйте репозиторий
git clone https://github.com/your-username/habit-tracker.git
cd habit-tracker

# 2. Соберите Docker-образ
docker build -t habit-tracker-app .

# 3. Запустите контейнер
docker run -d -p 8000:8000 --name solvit_tracker_container habit-tracker-app
```

*После запуска бэкенд будет доступен по адресу `http://localhost:8000`.*

**Управление контейнером:**
* Остановить контейнер: `docker stop solvit_tracker_container`
* Запустить снова: `docker start solvit_tracker_container`
* Удалить контейнер: `docker rm solvit_tracker_container`

---

### Вариант 2: Локальный запуск (Классический) 💻

```bash
# 1. Клонируйте репозиторий и перейдите в папку
git clone https://github.com/your-username/habit-tracker.git
cd habit-tracker

# 2. Создайте и активируйте виртуальное окружение
python -m venv venv

# Для Windows:
venv\Scripts\activate
# Для macOS / Linux:
source venv/bin/activate

# 3. Установите зависимости
pip install -r requirements.txt

# 4. Запустите сервер разработки Uvicorn
uvicorn src.main:app --reload
```

---

## 🧭 Проверка работы и адреса

После запуска бэкенда (любым из способов) проект доступен по следующим адресам:
* **🌐 API Server:** `http://localhost:8000`
* **📑 Interactive OpenAPI (Swagger) Docs:** `http://localhost:8000/docs`

### 💽 Инициализация Базы Данных

> [!IMPORTANT]
> Перед началом работы с приложением обязательно выполните инициализацию БД!
> Без выполнения этого шага таблицы в базе данных не будут созданы, и эндпойнты работы с привычками будут возвращать ошибку сервера.

В проекте реализован служебный эндпойнт для автоматического создания (или полной пересборки) метаданных базы данных. Отправьте POST-запрос на эндпойнт `/setup_database` одним из способов:

#### Способ 1: Через Swagger UI (Рекомендуется)
1. Перейдите по адресу [http://localhost:8000/docs](http://localhost:8000/docs).
2. Раскройте тег `Установка Базы Данных 💽`.
3. Нажмите **Try it out** ➔ **Execute**.
   
#### Способ 2: Через cURL
```bash
curl -X 'POST' 'http://localhost:8000/setup_database' -H 'accept: application/json'
```

> [!WARNING]
> Данный метод выполняет `drop_all` и `create_all`. Вызов метода полностью очищает существующую БД и создает структуру с нуля!

---

### 🚀 Запуск Фронтенда

Фронтенд полностью автономен и не требует сборки (Webpack/Vite не нужны).

1. Убедитесь, что сервер FastAPI запущен (в Docker или локально) и принимает запросы на `http://localhost:8000`.
2. Откройте файл `index.html` прямо в вашем браузере (двойным кликом из проводника или через расширение Live Server в VS Code).

   
### 📌 Документация REST API

| Метод | HTTP Эндпойнт | Тег / Раздел | Описание |
| :---: | :--- | :--- | :--- |
| `POST` | `/setup_database` | `Установка Базы Данных 💽` | Инициализация / Сброс таблиц базы данных |
| `GET` | `/habits` | `Привычки 🚬` | Получить список всех привычек |
| `POST` | `/habits` | `Привычки 🚬` | Добавить новую привычку |
| `GET` | `/habits/{habit_id}` | `Привычки 🚬` | Получить подробную информацию о привычке по ID |
| `PUT` | `/habits/{habit_id}` | `Привычки 🚬` | Обновить название и описание привычки |
| `PATCH` | `/habits/{habit_id}/toggle` | `Привычки 🚬` | Переключить статус выполнения (`checking`) |
| `DELETE` | `/habits/{habit_id}` | `Привычки 🚬` | Удалить привычку по ID |


## 📂 Структура проекта
```
habit_tracker/
├── database
│   ├── __init__.py
│   └── function.py
├── Dockerfile
├── index.html
├── README.md
├── requirements.txt
├── src
│   ├── api
│   │   ├── __init__.py
│   │   ├── dependencies.py
│   │   ├── function.py
│   │   └── habits.py
│   ├── database.py
│   ├── main.py
│   ├── models
│   │   └── habits.py
│   └── schemas
│       └── habits.py
```
