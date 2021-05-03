"""
Dag using the newly introduced TaskFlow API.
"""

import json

from airflow.decorators import dag, task
from airflow.utils.dates import days_ago

default_args = {
    "owner": "airflow"
}


# We are using a `dag` decorator to define the whole pipeliine
# Then, each function with a `task` decorator will be each of the
# work units that will be performed within the DAG. The function name is the
# unique identifier of the task.
@dag(
    "dag002",
    default_args=default_args,
    schedule_interval=None,
    start_date=days_ago(2),
    tags=["dag002"])
def tutorial_taskflow_api_etl():
    """
    Simple ETL pipeline which demonstrates the use of TaskFlow API.
    """

    @task()
    def extract():
        data_string = '{"1001": 301.27, "1002": 433.21, "1003": 502.22}'
        order_data_dict = json.loads(data_string)
        return order_data_dict

    # Tasks may infer that they return multiple outputs by passing a dict
    # As we don't want the following task to return multiple outputs
    # we set the flag to `False`

    @task(multiple_outputs=False)
    def transform(order_data_dict: dict):
        total_order_value = 0
        for value in order_data_dict.values():
            total_order_value += value
        return {"total_order_value": total_order_value}

    @task()
    def load(total_order_value: float):
        print("Total order value is: %.2f" % total_order_value)

    # Here we define the main flow of the DAG. We invoke the previous tasks in
    # the logical order that we want the DAG to execute. The dependencies
    # between tasks and the data exchanged are all handled by Airflow.
    # This is because each of the tasks may
    # run in different workers on different nodes on the network/cluster.
    order_data = extract()
    order_summary = transform(order_data)
    load(order_summary["total_order_value"])


tutorial_etl_dag_with_taskflow_api = tutorial_taskflow_api_etl()


"""
But what if we had a BashOperator or FileSensor based tasks 
before our python-based tasks?

```python
@task()
def extract_from_file()
    order_data_file = "/tmp/order_data.csv"
    order_data_df = pd.read_csv(order_data_file)

# The Sensor tasks wait for the file.
file_task = FileSensor(task_id="check_file", filepath="/tmp/order_data.csv")
order_data = extract_from_file()

file_task >> order_data
```
"""
