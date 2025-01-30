Проект включает в себя базовую структуру для создания RESTful API с использованием FastAPI. Ветка `develop` содержит актуальные изменения и доработки, которые находятся в процессе разработки.

Шаги по запуску:

1.pip install -r req.txt
2. Создаем папку с миграциями alembic init alembic
3. Создаем миграцию таблиц lembic revision --autogenerate -m "comment"
4. Применяем миграцию alembic upgrade head 
5. оборачиваем все в докер, значения в {} заменить на свои docker run -d --name {container-name} -p 50ХХ:5432 -e POSTGRES_DB={db-name} -e POSTGRES_USER={username} -e POSTGRES_PASSWORD={password} postgres:15.2 
6.  запускаем проет uvicorn app.main:app
7. переходим по ссылке http://127.0.0.1:8000/docs/

Ендпоинты:
1. GET /Home page - домашняя страница, проект запущен
2. POST/auth/register - регистрация пользователя
3. POST/auth/login - авторизация пользователя
4. GET /auth/me - получение данных о пользователе, работает только если авторизирован
5. POST/auth/logout - выход из аккаунта

