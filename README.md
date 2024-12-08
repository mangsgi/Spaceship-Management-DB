# Spaceship-Management-DB
2024-2 Database Term Project Spaceship Management Database System

```shell
# if you want to execute backend
uvicorn main:app --port 8000

# if you want to execute frontend
npm run dev

# database reset
DROP DATABASE spacedb;
GRANT ALL PRIVILEGES ON DATABASE spacedb TO common;
```