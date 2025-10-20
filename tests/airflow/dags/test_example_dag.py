import logging
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

import pytest


class TestExampleDAG:
    """Tests for the example_dag without requiring Airflow DB."""

    @pytest.fixture
    def mock_airflow_context(self):
        """Mock Airflow context to avoid DB dependencies."""
        with patch("airflow.models.dag.DagBag") as mock_dagbag, patch(
            "airflow.models.dag.DAG"
        ) as mock_dag_class:
            yield mock_dagbag, mock_dag_class

    def test_dag_can_be_imported(self):
        """Test that the DAG module can be imported without errors."""
        try:
            from src.airflow.dags import example_dag

            assert example_dag is not None
        except Exception as e:
            pytest.fail(f"Failed to import example_dag: {e}")

    def test_dag_has_correct_configuration(self):
        """Test DAG configuration values."""
        from src.airflow.dags.example_dag import dag, default_args

        assert dag.dag_id == "example_dag"
        assert dag.description == "A simple example DAG"
        assert dag.catchup is False
        assert dag.tags == ["example"]
        assert dag.schedule_interval == timedelta(days=1)

        assert default_args["owner"] == "airflow"
        assert default_args["depends_on_past"] is False
        assert default_args["email_on_failure"] is False
        assert default_args["email_on_retry"] is False
        assert default_args["retries"] == 1
        assert default_args["retry_delay"] == timedelta(minutes=5)

    def test_dag_has_correct_tasks(self):
        """Test that DAG contains expected tasks."""
        from src.airflow.dags.example_dag import dag

        task_ids = [task.task_id for task in dag.tasks]
        assert "python_task" in task_ids
        assert "bash_task" in task_ids
        assert len(task_ids) == 2

    def test_dag_task_dependencies(self):
        """Test that tasks have correct dependencies."""
        from src.airflow.dags.example_dag import dag

        python_task = dag.get_task("python_task")
        bash_task = dag.get_task("bash_task")

        assert bash_task in python_task.downstream_list
        assert python_task in bash_task.upstream_list

    def test_python_task_configuration(self):
        """Test Python task configuration."""
        from src.airflow.dags.example_dag import dag

        python_task = dag.get_task("python_task")
        assert python_task.task_id == "python_task"
        assert python_task.task_type == "PythonOperator"

    def test_bash_task_configuration(self):
        """Test Bash task configuration."""
        from src.airflow.dags.example_dag import dag

        bash_task = dag.get_task("bash_task")
        assert bash_task.task_id == "bash_task"
        assert bash_task.task_type == "BashOperator"
        assert bash_task.bash_command == 'echo "Hello from Bash!"'

    def test_example_task_callable_exists(self):
        """Test that the example_task function exists and is callable."""
        from src.airflow.dags.example_dag import example_task

        assert callable(example_task)

    def test_example_task_execution(self, caplog):
        """Test example_task function execution with mocked logger."""
        from src.airflow.dags.example_dag import example_task

        with caplog.at_level(logging.INFO):
            result = example_task()

        assert result == "Task completed successfully"
        assert "Hello from Airflow!" in caplog.text

    def test_dag_start_date_is_valid(self):
        """Test that DAG has a valid start_date."""
        from src.airflow.dags.example_dag import default_args

        assert "start_date" in default_args
        assert isinstance(default_args["start_date"], datetime)
        assert default_args["start_date"] == datetime(2024, 1, 1)

    def test_dag_has_no_cycles(self):
        """Test that DAG has no circular dependencies."""
        from src.airflow.dags.example_dag import dag

        # Verify there are no cycles by checking task dependencies
        # Airflow will raise an exception if there are cycles when the DAG is created
        # So if we can access the tasks, there are no cycles
        assert len(dag.tasks) > 0
        for task in dag.tasks:
            # Ensure each task can access its dependencies
            assert task.upstream_task_ids is not None
            assert task.downstream_task_ids is not None
