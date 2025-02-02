# Сервис покупки для авторизированных пользователей

Проект включает в себя базовую структуру для создания RESTful API с использованием FastAPI.
Ветка `main` содержит актуальные изменения и доработки, которые находятся в процессе разработки.

## Шаги по запуску:

1. Устанавливаем необходимые зависимости: pip install -r req.txt 
2. Применяем миграцию: alembic upgrade head 
3. Оборачиваем все в докер, значения в {} заменить на свои: docker run -d --name {container-name} -p 50ХХ:5432 -e POSTGRES_DB={db-name} -e POSTGRES_USER={username} -e POSTGRES_PASSWORD={password} postgres:15.2 
4. Запускаем проект: uvicorn app.main:app 
5. Переходим по ссылке: http://127.0.0.1:8000/docs/
