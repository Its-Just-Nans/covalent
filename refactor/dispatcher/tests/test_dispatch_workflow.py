# Copyright 2021 Agnostiq Inc.
#
# This file is part of Covalent.
#
# Licensed under the GNU Affero General Public License 3.0 (the "License").
# A copy of the License may be obtained with this software package or at
#
#      https://www.gnu.org/licenses/agpl-3.0.en.html
#
# Use of this file is prohibited except in compliance with the License. Any
# modifications or derivative works of this file must retain this copyright
# notice, and modified files must contain a notice indicating that they have
# been altered from the originals.
#
# Covalent is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the License for more details.
#
# Relief from the License may be granted by purchasing a commercial license.

"""Unit tests for dispatching workflows."""

from copy import deepcopy
from datetime import datetime, timezone

import pytest
from app.core.dispatch_workflow import (
    dispatch_runnable_tasks,
    dispatch_workflow,
    get_runnable_tasks,
    init_result_pre_dispatch,
    is_runnable_task,
    run_tasks,
    start_dispatch,
)

import covalent as ct
from covalent._results_manager.result import Result
from covalent._workflow.transport import TransportableObject, _TransportGraph
from covalent.executor import BaseExecutor


@pytest.fixture
def mock_result_uninitialized():
    """Construct mock result object."""

    @ct.electron
    def add(x, y):
        return x + y

    @ct.electron
    def multiply(x, y):
        return x * y

    @ct.electron
    def square(x):
        return x**2

    @ct.lattice
    def workflow(x, y, z):

        a = add(x, y)
        b = square(z)
        final = multiply(a, b)
        return final

    lattice = deepcopy(workflow)
    lattice.build_graph(x=1, y=2, z=3)
    lattice.transport_graph = lattice.transport_graph.serialize()

    return Result(lattice=lattice, results_dir="", dispatch_id="mock_dispatch_id")


@pytest.fixture
def mock_result_initialized(mock_result_uninitialized):
    """Construct mock result object."""

    result_obj = deepcopy(mock_result_uninitialized)

    init_result_pre_dispatch(result_obj)
    return result_obj


@pytest.fixture
def mock_tasks_queue():
    """Construct mock tasks queue."""

    from multiprocessing import Queue as MPQ

    return MPQ()


@pytest.mark.parametrize(
    "initial_status,start_dispatch_call_status",
    [
        (Result.NEW_OBJ, True),
        (Result.COMPLETED, False),
        (Result.RUNNING, False),
        (Result.FAILED, False),
    ],
)
def test_dispatch_workflow_func(
    mocker, mock_result_initialized, mock_tasks_queue, initial_status, start_dispatch_call_status
):
    """Test that the dispatch workflow function calls the appropriate method depending on the result object status."""

    mock_update_result_obj = mocker.Mock()
    mock_start_dispatch = mocker.patch(
        "app.core.dispatch_workflow.start_dispatch",
        return_value=mock_update_result_obj,
    )

    mock_result_initialized._status = initial_status

    result_obj = dispatch_workflow(
        result_obj=mock_result_initialized, tasks_queue=mock_tasks_queue
    )

    if start_dispatch_call_status:
        mock_start_dispatch.assert_called_once_with(
            result_obj=mock_result_initialized, tasks_queue=mock_tasks_queue
        )
        assert result_obj == mock_update_result_obj

    assert mock_start_dispatch.called is start_dispatch_call_status


def test_start_dispatch(mocker, mock_result_initialized, mock_tasks_queue):
    """Test the start_dispatch method which kicks of the workflow execution."""

    mock_result_init = mocker.patch(
        "app.core.dispatch_workflow.init_result_pre_dispatch",
        return_value=mock_result_initialized,
    )
    mock_send_result = mocker.patch(
        "app.core.dispatch_workflow.send_result_object_to_result_service"
    )
    mocker.patch(
        "app.core.dispatch_workflow.get_task_order",
        return_value=[[0], [1, 2, 3], [4, 5], [6]],
    )
    mock_dispatch_runnable_tasks = mocker.patch(
        "app.core.dispatch_workflow.dispatch_runnable_tasks"
    )

    result_obj = start_dispatch(mock_result_initialized, mock_tasks_queue)

    assert result_obj.status == Result.RUNNING
    assert result_obj.start_time is not None

    mock_result_init.assert_called_once_with(mock_result_initialized)
    assert mocker.call(mock_result_initialized) in mock_send_result.mock_calls
    assert len(mock_send_result.mock_calls) == 2
    mock_dispatch_runnable_tasks.assert_called_once_with(
        mock_result_initialized, mock_tasks_queue, [[0], [1, 2, 3], [4, 5], [6]]
    )


def test_init_result_pre_dispatch(mocker, mock_result_uninitialized):
    """Test the result object initialization method."""

    mock_initialize_nodes = mocker.patch(
        "covalent._results_manager.result.Result._initialize_nodes"
    )

    assert isinstance(mock_result_uninitialized.lattice.transport_graph, bytes)

    post_init_result_obj = init_result_pre_dispatch(mock_result_uninitialized)
    assert isinstance(post_init_result_obj.lattice.transport_graph, _TransportGraph)

    mock_initialize_nodes.assert_called_once_with()


def test_run_tasks(mocker):
    """Test the method that sends tasks to the Runner service for execution."""

    mock_send_task_list_to_runner = mocker.patch(
        "app.core.dispatch_workflow.send_task_list_to_runner", return_value=[2]
    )

    mock_results_dir = "mock_results_dir"
    mock_dispatch_id = "mock_dispatch_id"

    unrun_tasks = run_tasks(
        results_dir=mock_results_dir,
        dispatch_id=mock_dispatch_id,
        task_id_batch=[1, 2],
        functions=[b"f1", b"f2"],
        input_args=[{}, {}],
        input_kwargs=[{}, {}],
        executors=[b"e1", b"e2"],
    )

    mock_task_list = [
        {
            "task_id": 1,
            "func": b"f1",
            "args": {},
            "kwargs": {},
            "executor": b"e1",
            "results_dir": "mock_results_dir",
        },
        {
            "task_id": 2,
            "func": b"f2",
            "args": {},
            "kwargs": {},
            "executor": b"e2",
            "results_dir": "mock_results_dir",
        },
    ]

    assert (
        mocker.call(dispatch_id="mock_dispatch_id", tasks_list=mock_task_list)
        in mock_send_task_list_to_runner.mock_calls
    )

    assert unrun_tasks == [2]


@pytest.mark.parametrize(
    "node_0_status,node_3_status,expected_runnable_status",
    [
        (Result.RUNNING, Result.RUNNING, False),
        (Result.COMPLETED, Result.RUNNING, False),
        (Result.FAILED, Result.RUNNING, False),
        (Result.COMPLETED, Result.COMPLETED, True),
    ],
)
def test_is_runnable_task(
    mock_result_initialized, node_0_status, node_3_status, expected_runnable_status
):
    """Test function that returns status of whether a task is runnable."""

    result_obj = mock_result_initialized
    result_obj.lattice.transport_graph.set_node_value(0, "status", node_0_status)
    result_obj.lattice.transport_graph.set_node_value(3, "status", node_3_status)

    assert is_runnable_task(task_id=5, result_obj=result_obj) == expected_runnable_status


def test_get_runnable_tasks_lattice(mocker, mock_result_initialized, mock_tasks_queue):
    """Test get_runnable_tasks method."""

    # Tasks order of mock workflow - [[1, 2, 4], [0, 3], [5]]
    mock_tasks_order = (
        mock_result_initialized.lattice.transport_graph.get_topologically_sorted_graph()
    )
    mock_tasks_queue.put([{mock_result_initialized.dispatch_id: mock_tasks_order}])

    (
        runnable_tasks,
        functions,
        input_args,
        input_kwargs,
        executors,
        next_tasks_order,
    ) = get_runnable_tasks(
        result_obj=mock_result_initialized,
        tasks_order=mock_tasks_order,
        tasks_queue=mock_tasks_queue,
    )

    assert runnable_tasks == [0, 3]
    assert isinstance(functions[0], TransportableObject)
    assert isinstance(functions[1], TransportableObject)
    assert input_args == [[1, 2], [3]]
    assert input_kwargs == [{}, {}]
    assert isinstance(executors[0], BaseExecutor)
    assert isinstance(executors[1], BaseExecutor)
    assert next_tasks_order == [[5]]

    _, _, _, _, _, next_tasks_order = get_runnable_tasks(
        result_obj=mock_result_initialized,
        tasks_order=next_tasks_order,
        tasks_queue=mock_tasks_queue,
    )

    # Since the task statuses of [0, 3] have not been changed to completed, task 5 should not be runnable.
    assert next_tasks_order == [[5]]

    # Update node results to ensure that task 5 becomes runnable
    mock_result_initialized._update_node(
        node_id=0,
        end_time=datetime.now(timezone.utc),
        status=Result.COMPLETED,
    )
    mock_result_initialized._update_node(
        node_id=3,
        end_time=datetime.now(timezone.utc),
        status=Result.COMPLETED,
    )

    mock_tasks_queue.get()
    mock_tasks_queue.put(next_tasks_order)

    _, _, _, _, _, next_tasks_order = get_runnable_tasks(
        result_obj=mock_result_initialized,
        tasks_order=next_tasks_order,
        tasks_queue=mock_tasks_queue,
    )

    assert next_tasks_order == []


@pytest.mark.parametrize(
    "unrun_tasks,expected_mock_tasks_queue",
    [
        ([3], [{"mock_dispatch_id": [[3], [5]]}]),
        ([0, 3], [{"mock_dispatch_id": [[0, 3], [5]]}]),
        ([], [{"mock_dispatch_id": [[5]]}]),
    ],
)
def test_dispatch_runnable_tasks(
    mocker, mock_result_initialized, mock_tasks_queue, unrun_tasks, expected_mock_tasks_queue
):
    """Test the dispatch_runnable_tasks method."""

    mock_get_runnable_tasks = mocker.patch(
        "app.core.dispatch_workflow.get_runnable_tasks",
        return_value=(
            [0, 3],
            [b"f0", b"f3"],
            [[1, 2], [3]],
            [{}, {}],
            ["BaseExecutor", "BaseExecutor"],
            [[5]],
        ),
    )
    mock_run_tasks = mocker.patch("app.core.dispatch_workflow.run_tasks", return_value=unrun_tasks)

    dispatch_runnable_tasks(
        result_obj=mock_result_initialized,
        tasks_queue=mock_tasks_queue,
        task_order=[[1, 2, 4], [0, 3], [5]],
    )

    val = mock_tasks_queue.get()
    assert val == expected_mock_tasks_queue


# TODO
def test_get_runnable_tasks_sublattice():
    pass


# TODO
def test_dispatch_runnable_tasks_sublattice():
    pass
