"""
Running Airflow on local.

Airflow scripts are just configuration files specifying the DAG's structure.

Different tasks run on different workers at different points in time, which means that this 
script cannot be used to cross communicate between tasks.
"""
from datetime import timedelta
from textwrap import dedent

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

# These arguments will be passed to all of the operators.
# It's also possible to define different sets of arguments depending
# on the environment they're executed on.
# (Development or production for example)
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email": ["manumg8@gmail.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5)
}

# We use an instantiated DAG as a context manager. The first string
# is the DAG Id, which serves to uniquely identify your DAG.
with DAG(
    "dag001",
    default_args=default_args,
    description="A simple tutorial DAG",
    schedule_interval=timedelta(days=1),  # Will be executed daily
    start_date=days_ago(2),
    tags=["example"]
) as dag:

    # Tasks are instantiated from an Operator object. An instantiated
    # object is a task.
    t1 = BashOperator(
        task_id="print_date",
        bash_command="date"
    )

    t2 = BashOperator(
        task_id="sleep",
        depends_on_past=False,
        bash_command="sleep 5",
        retries=3
    )

    dag.doc_md = __doc__
    t1.doc_md = dedent(
        """\
    #### Task Documentation
    You can document your task using the attributes `doc_md` (markdown),
    `doc` (plain text), `doc_rst`, `doc_json`, `doc_yaml` which gets
    rendered in the UI's Task Instance Details page.

    ![img](http://montcs.bloomu.edu/~bobmon/Semesters/2012-01/491/import%20soul.png)
    """
    )

    # Ninja Templating. It provides a set of built-in parameters and macros.
    # Airflow also provides hooks for the pipeline author to define their own
    # parameters, macros and templates. `ds` is today's date stamp.
    # The `params` hook in BashOperator allows you to pass a dictionary of
    # parameters and/or objects to your templates.
    # Files can also be passed to the `bash_command`
    # argument as `bash_command='templated_command.sh'`,
    # where the file location
    # is relative to the directory containing the pipeline file (tutorial.py)
    templated_command = dedent(
        """
    {% for i in range(5) %}
        echo "{{ ds }}"
        echo "{{ macros.ds_add(ds, 7) }}"
        echo "{{ params.my_param }}
    {% endfor %}
        """
    )

    t3 = BashOperator(
        task_id="templated",
        depends_on_past=False,
        bash_command=templated_command,
        params={
            "my_param": "Parameter I passed in"
        }
    )

    t1 >> [t2, t3]

    # Different types of tasks dependencies
    """
    This means that t2 will depend on t1 running successfully to run
    t1.set_downstream(t2)

    This operator is used to chain operations
    t1 >> t2

    This opeartor is used for upstream dependency
    t2 << t1
    """
    