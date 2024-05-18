# Механизм доставки, обработки и хранения данных 
## Структура проекта:
1. Backup_DB - код для стриминговой доставки (PostgreSQL -> Debezium + Kafka -> ClickHouse)
  - Data_Preparing - код для предобработки данных перед добавлением в PostgreSQL
  - Postgres_DB - работа с Postgres 
    - python_scripts - добавление данных в таблицы
    - sql_scripts - sql - код для создания и редактирования таблиц
  - Debezium_Kafka - код для Debezium + Kafka
    - Debezium - конфиг настройки Debezium
    - Kafka - код для тестов Kafka
  - ClickHouse - код для создания и редактирования таблиц в ClickHouse
2. Object_Storage - код для доставки изображений в Minio
3. Additional_Tables - код для пакетной обработки данных с AirFlow
   - SQL_Examples - код для обработки данных при помощи SQL
   - Spark_Examples - код для обработки данных при помощи Spark




