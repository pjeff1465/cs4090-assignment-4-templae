'''
import pytest
from hypothesis import given
from hypothesis.strategies import text


# used to test edge cases with randomized inputs
# Edge testing


@given(text())
def test_task_random_input(title):
   result = some_function(title)
   '''

import pytest
import tempfile

from hypothesis import given
from hypothesis.strategies import lists, integers, dictionaries, just, text, sampled_from
from tasks import *


@given(
    lists(dictionaries(keys=just("description"), values=text()), min_size=1),
    text()
)
def test_search_tasks_does_not_crash(tasks, query):
    # Safely enrich each task to ensure both fields exist
    enriched_tasks = [
        {"title": "", "description": task.get("description", "")}
        for task in tasks
    ]
    results = search_tasks(enriched_tasks, query)
    assert isinstance(results, list)


@given(
    lists(
        dictionaries(keys=just("priority"), values=text() | integers()),
        min_size=1
    ),
    text()
)
def test_edge_filter_tasks_by_priority(tasks, priority):
    result = filter_tasks_by_priority(tasks, priority)
    assert isinstance(result, list)

@given(
    lists(dictionaries(keys=text(), values=text() | integers()), min_size=1)
)
def test_edge_save_then_load(tasks):
    save_tasks(tasks, "test_tasks.json")
    loaded = load_tasks("test_tasks.json")
    assert isinstance(loaded, list)


@given(
    lists(dictionaries(keys=text(), values=text()), min_size=1)
)
def test_edge_generate_unique_id(tasks):
    try:
        generate_unique_id(tasks)
    except KeyError:
        assert False, "generate_unique_id crashed due to missing 'id'"

# check if code will crash with messy input priority data
@given(
    lists(
        dictionaries(
            keys=text(),
            values=text(),
            min_size=0,
            max_size=5
        ),
        min_size=1
    ),
    sampled_from(["High", "Medium", "Low"])
)
def test_edge_filter_task_priority(tasks, priority):
    try:
        result = filter_tasks_by_priority(tasks, priority)
        assert isinstance(result, list)
    except Exception as e:
        assert False, f"filter_tasks_by_priority crashed with invalid task data format: {e}"
