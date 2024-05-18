# Механизм доставки, обработки и хранения данных 
## Структура проекта
  1_Backup_DB - код для стриминговой доставки (PostgreSQL -> Debezium + Kafka -> ClickHouse)
    1_Data_Preparing - код для предобработки данных перед добавлением в PostgreSQL
    2_Postgres_DB - работа с Postgres 
      python_scripts - добавление данных в таблицы
      sql_scripts - sql - код для создания и редактирования таблиц
    3_Debezium_Kafka - код для Debezium + Kafka
      Debezium - конфиг настройки Debezium
      Kafka - код для тестов Kafka
    4_ClickHouse - код для создания и редактирования таблиц в ClickHouse
  2_Object_Storage - код для доставки изображений в Minio
  3_Additional_Tables - код для пакетной обработки данных с AirFlow
    SQL_Examples - код для обработки данных при помощи SQL
    Spark_Examples - код для обработки данных при помощи Spark
  docker-compose.yml - общий docker-compose-файл для всего механизма

