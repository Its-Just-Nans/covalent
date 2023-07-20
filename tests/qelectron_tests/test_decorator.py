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

# pylint: disable=no-member

import copy
import random

import pennylane as qml
import pytest
from numpy import isclose

import covalent as ct

EXECUTORS = [
    ct.executor.QiskitExecutor(device="local_sampler", shots=10_000),
]


@pytest.mark.parametrize("executor", EXECUTORS)
def test_decorator_vs_explicit_wrapper(executor):
    """
    Test that `ct.qelectron` works as decorator and as explicit wrapper.
    """

    results = []

    # Initialize qelectron by decorating a qnode.
    dev = qml.device("default.qubit", wires=2)

    @ct.qelectron(executors=executor)
    @qml.qnode(device=dev)
    def simple_circuit_1(param):
        """
        A tiny, reusable Pennylane circuit.
        """
        qml.RX(param, wires=0)
        qml.Hadamard(wires=1)
        qml.CNOT(wires=[0, 1])
        return qml.expval(qml.operation.Tensor(*(qml.PauliY(0), qml.PauliX(1))))

    qelectron = simple_circuit_1
    results.append(qelectron(0.5))

    # Initialize qelectron by passing a qnode.
    @qml.qnode(device=dev)
    def simple_circuit_2(param):
        """
        A tiny, reusable Pennylane circuit.
        """
        qml.RX(param, wires=0)
        qml.Hadamard(wires=1)
        qml.CNOT(wires=[0, 1])
        return qml.expval(qml.operation.Tensor(*(qml.PauliY(0), qml.PauliX(1))))

    qelectron = ct.qelectron(simple_circuit_2, executors=executor)
    results.append(qelectron(0.5))

    assert isinstance(results[0], type(results[1])), f"Results {results!r} are not the same type"
    assert isclose(results[0], results[1], 0.1), f"Results {results!r} are not close"


class TestDecoratorArguments:
    """
    Test that the `ct.qelectron` decorator accepts and correctly processes various
    types of `executors` arguments.

    Specifically, the following types should be supported and the corresponding
    behavior observed:

    (1) `executors=executor_1`
        -> a single executor is used for all circuits

    (2) `executors=[executor_1, ..., executor_N]`
        -> a `QCluster` is created from the two or more executor instances

    (3) `executors=qcluster_1`
        -> the given `QCluster` is used for all circuits
    """

    @pytest.mark.parametrize("executor", EXECUTORS)
    def test_single_executor(self, executor):
        """
        Test that the `ct.qelectron` decorator accepts a single executor (case 1).
        """

        dev = qml.device("default.qubit", wires=2)

        # QElectron definition.
        @ct.qelectron(executors=executor)
        @qml.qnode(device=dev)
        def qelectron_circuit(param):
            qml.RX(param, wires=0)
            qml.Hadamard(wires=1)
            qml.CNOT(wires=[0, 1])
            return qml.expval(qml.operation.Tensor(*(qml.PauliY(0), qml.PauliX(1))))

        # Equivalent QNode definition (for comparison).
        @qml.qnode(device=dev)
        def normal_circuit(param):
            qml.RX(param, wires=0)
            qml.Hadamard(wires=1)
            qml.CNOT(wires=[0, 1])
            return qml.expval(qml.operation.Tensor(*(qml.PauliY(0), qml.PauliX(1))))

        res = normal_circuit(0.5)
        qres = qelectron_circuit(0.5)

        assert isinstance(qres, type(res)), f"Results {res!r} and {qres!r} are not the same type"
        assert isclose(qres, res, 0.1), f"Results {res!r} and {qres!r} are not close"

    @pytest.mark.parametrize("executor", EXECUTORS)
    def test_list_of_executors(self, executor):
        """
        Test that the `ct.qelectron` decorator accepts a list of executors (case 2).
        """

        dev = qml.device("default.qubit", wires=2)

        # Create a list of executors.
        executors_list = [executor, copy.deepcopy(executor)]

        # QElectron definition.
        @ct.qelectron(executors=executors_list)
        @qml.qnode(device=dev)
        def qelectron_circuit(param):
            qml.RX(param, wires=0)
            qml.Hadamard(wires=1)
            qml.CNOT(wires=[0, 1])
            return qml.expval(qml.operation.Tensor(*(qml.PauliY(0), qml.PauliX(1))))

        # Check that the executor is a `QCluster`.
        assert len(qelectron_circuit.device.executors) == 1
        assert isinstance(qelectron_circuit.device.executors[0], ct.executor.QCluster)

        # Equivalent QNode definition (for comparison).
        @qml.qnode(device=dev)
        def normal_circuit(param):
            qml.RX(param, wires=0)
            qml.Hadamard(wires=1)
            qml.CNOT(wires=[0, 1])
            return qml.expval(qml.operation.Tensor(*(qml.PauliY(0), qml.PauliX(1))))

        res = normal_circuit(0.5)
        qres = qelectron_circuit(0.5)

        assert isinstance(qres, type(res)), f"Results {res!r} and {qres!r} are not the same type"
        assert isclose(qres, res, 0.1), f"Results {res!r} and {qres!r} are not close"

    @pytest.mark.parametrize("executor", EXECUTORS)
    def test_explicit_qcluster(self, executor):
        """
        Test that the `ct.qelectron` decorator accepts a `QCluster` instance (case 3).
        """

        dev = qml.device("default.qubit", wires=2)

        # Create a `QCluster` explicitly.
        executors_list = [executor, copy.deepcopy(executor)]
        qcluster = ct.executor.QCluster(executors=executors_list)

        # QElectron definition.
        @ct.qelectron(executors=qcluster)
        @qml.qnode(device=dev)
        def qelectron_circuit(param):
            qml.RX(param, wires=0)
            qml.Hadamard(wires=1)
            qml.CNOT(wires=[0, 1])
            return qml.expval(qml.operation.Tensor(*(qml.PauliY(0), qml.PauliX(1))))

        # Check that the executor is a `QCluster`.
        assert len(qelectron_circuit.device.executors) == 1
        assert isinstance(qelectron_circuit.device.executors[0], ct.executor.QCluster)

        # Equivalent QNode definition (for comparison).
        @qml.qnode(device=dev)
        def normal_circuit(param):
            qml.RX(param, wires=0)
            qml.Hadamard(wires=1)
            qml.CNOT(wires=[0, 1])
            return qml.expval(qml.operation.Tensor(*(qml.PauliY(0), qml.PauliX(1))))

        res = normal_circuit(0.5)
        qres = qelectron_circuit(0.5)

        assert isinstance(qres, type(res)), f"Results {res!r} and {qres!r} are not the same type"
        assert isclose(qres, res, 0.1), f"Results {res!r} and {qres!r} are not close"
