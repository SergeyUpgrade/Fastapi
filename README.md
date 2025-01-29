Проект включает в себя базовую структуру для создания RESTful API с использованием FastAPI. Ветка `develop` содержит актуальные изменения и доработки, которые находятся в процессе разработки.

Шаги по запуску:

1.pip install -r req.txt
2. Создаем папку с миграциями alembic init migrations
3. Создаем миграцию таблиц lembic revision --autogenerate -m "comment"
4. Применяем миграцию alembic upgrade head 
5. оборачиваем все в докер, значения в {} заменить на свои docker run -d --name {container-name} -p 50ХХ:5432 -e POSTGRES_DB={db-name} -e POSTGRES_USER={username} -e POSTGRES_PASSWORD={password} postgres:15.2 
6.  запускаем проет uvicorn app.main:app