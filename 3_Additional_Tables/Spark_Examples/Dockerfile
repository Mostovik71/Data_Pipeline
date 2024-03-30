FROM apache/airflow:2.5.2-python3.10

USER root

RUN DEBIAN_FRONTEND=noninteractive apt update && \
    apt-get install -y openjdk-17-jdk  && \
    apt-get install -y curl


WORKDIR /opt

RUN curl -o spark-3.4.2-bin-hadoop3.tgz https://dlcdn.apache.org/spark/spark-3.4.2/spark-3.4.2-bin-hadoop3.tgz
RUN tar -xzf spark-3.4.2-bin-hadoop3.tgz -C /opt
RUN rm spark-3.4.2-bin-hadoop3.tgz
RUN ln -sf /opt/spark-3.4.2-bin-hadoop3 /opt/spark

RUN curl -o clickhouse-jdbc-0.4.6.jar https://github.com/ClickHouse/clickhouse-java/releases/tag/v0.4.6/clickhouse-jdbc-0.4.6.jar

RUN mv clickhouse-jdbc-0.4.6.jar /opt/spark/jars

ENV JAVA_HOME /usr/lib/jvm/java-17-openjdk-amd64
ENV HADOOP_HOME /opt/spark
ENV SPARK_HOME /opt/spark

USER airflow

RUN pip install --upgrade pip && \
    pip install clickhouse-connect==0.7.3 &&\
    pip install pyspark==3.4.2
