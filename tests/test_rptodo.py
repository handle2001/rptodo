"""Tests for the RP To-do app"""

# tests/test_rptodo.py
import json

import pytest
from typer.testing import CliRunner

from rptodo import DB_READ_ERROR, SUCCESS, __app_name__, __version__, cli, rptodo

test_data1 = {
    "description": ["Clean", "the", "house"],
    "priority": 1,
    "todo": {
        "Description": "Clean the house.",
        "Priority": 1,
        "Done": False,
    },
}
test_data2 = {
    "description": ["Wash the car"],
    "priority": 2,
    "todo": {
        "Description": "Wash the car.",
        "Priority": 2,
        "Done": False,
    },
}


@pytest.fixture
def mock_json_file(tmp_path):
    """Setup a mock json file for testing purposes"""
    todo = [
        {
            "Description": "Get some milk",
            "Priority": 2,
            "Done": False,
        },
    ]
    db_file = tmp_path / "todo.json"
    with db_file.open("w") as db:
        json.dump(todo, db, indent=4)
    return db_file


@pytest.mark.parametrize(
    "description, priority, expected",
    [
        pytest.param(
            test_data1["description"],
            test_data1["priority"],
            (test_data1["todo"], SUCCESS),
        ),
        pytest.param(
            test_data2["description"],
            test_data2["priority"],
            (test_data2["todo"], SUCCESS),
        ),
    ],
)
def test_add(mock_json_file, description, priority, expected):
    """Test adding a new to-do"""
    todoer = rptodo.Todoer(mock_json_file)
    assert todoer.add(description, priority) == expected
    read = todoer._db_handler.read_todos()
    assert len(read.todo_list) == 2


runner = CliRunner()
# CliRunner is used to test the app's command line interface
# Like Selenium but for the terminal


def test_version():
    """Test printing the version from command line"""
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} v{__version__}\n" in result.stdout
