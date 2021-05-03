# airflow
Repository containing learning resources for Airflow. 


## Set up Airflow in Local Kubernetes Cluster
Reference 1: https://marclamberti.com/blog/running-apache-airflow-locally-on-kubernetes/
Reference 2: https://gtoonstra.github.io/etl-with-airflow/platform.html

## Set up Airflow in Local Mode

```bash
export AIRFLOW_HOME=~/airflow
AIRFLOW_VERSION=2.0.1
PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-3.7.txt"
pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"

# Initialize the database
airflow db init

airflow users create \
    --username admin \
    --firstname Peter \
    --lastname Parker \
    --role Admin \
    --email spiderman@superhero.org

# start the web server, default port is 8080
airflow webserver --port 8080

# start the scheduler
# open a new terminal or else run webserver with ``-D`` option to run it as a daemon
airflow scheduler

# visit localhost:8080 in the browser and use the admin account you just
# created to login. Enable the example_bash_operator dag in the home page
```

> Every time we create a new DAG `Python` script, we have to restart the databse doing: `airflow db init`.
> Furthermore, the scripts should be located within the given `AIRFLOW_HOME`.
