FROM apache/airflow:2.9.1-python3.11


# Добавление apt пакетов
USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         vim \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Устанавливаем umask для правильного создания директорий
RUN umask 0002; \
  mkdir -p /opt/airflow/dags /opt/airflow/logs /opt/airflow/plugins
  
 # Создаем директории с нужными правами
RUN install -d -m 0755 -o airflow -g root /opt/airflow/dags/data

# Возвращаемся к пользователю airflow
USER airflow

# Добавление пакетов из PyPI
RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" lxml

# Добавление пакетов из requirements.txt
COPY requirements.txt /
RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" -r /requirements.txt
