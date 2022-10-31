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

"""Mock files data"""

import os
import pickle

from covalent._workflow.transport import TransportableObject, _TransportGraph

print("path ")
with open(
    os.path.dirname(os.path.abspath(__file__)) + "/sample_transport_graph", "rb"
) as sample_file:
    sample_data = pickle.load(sample_file)


def mock_files_data():
    """Mock files data"""
    transport_graph = _TransportGraph()
    transport_graph.lattice_metadata = {
        "executor": "dask",
        "results_dir": "/home/arunmukesh/Desktop/files/results",
        "workflow_executor": "dask",
        "deps": {},
        "call_before": [],
        "call_after": [],
        "executor_data": {},
        "workflow_executor_data": {},
    }
    transport_graph.dirty_nodes = []
    return {
        "lattice_files": {
            "path": "tests/covalent_ui_backend_tests/utils/mock_files/78525234-72ec-42dc-94a0-f4751707f9cd",
            "files": [
                {"file_name": "call_after.pkl", "data": []},
                {"file_name": "call_before.pkl", "data": []},
                {"file_name": "cova_imports.pkl", "data": {"electron", "ct"}},
                {"file_name": "deps.pkl", "data": {}},
                {"file_name": "error.log", "data": ""},
                {"file_name": "executor_data.pkl", "data": {}},
                {"file_name": "function_docstring.txt", "data": ""},
                {
                    "file_name": "function.pkl",
                    "data": TransportableObject.make_transportable(
                        "<function hello at 0x7fcc2cdb4670>"
                    ),
                },
                {
                    "file_name": "function_string.txt",
                    "data": """@ct.lattice
def workflow(name):
\tresult=join(hello(),moniker(name))
\treturn result+" !!\"""",
                },
                {
                    "file_name": "inputs.pkl",
                    "data": {
                        "args": [],
                        "kwargs": {"name": TransportableObject.make_transportable("shore")},
                    },
                },
                {
                    "file_name": "lattice_imports.pkl",
                    "data": """# import covalent as ct

                    """,
                },
                {"file_name": "named_args.pkl", "data": {}},
                {"file_name": "named_kwargs.pkl", "data": {}},
                {
                    "file_name": "results.pkl",
                    "data": TransportableObject.make_transportable("Hello shore  !!"),
                },
                {"file_name": "stderr.log", "data": ""},
                {"file_name": "stdout.log", "data": ""},
                {
                    "file_name": "transport_graph.pkl",
                    "data": sample_data,
                },
                {"file_name": "workflow_executor_data.pkl", "data": {}},
            ],
        },
        "electron_files_node_0": {
            "path": "tests/covalent_ui_backend_tests/utils/mock_files/78525234-72ec-42dc-94a0-f4751707f9cd/node_0",
            "files": [
                {"file_name": "call_after.pkl", "data": []},
                {"file_name": "call_before.pkl", "data": []},
                {
                    "file_name": "deps.pkl",
                    "data": {
                        "bash": {
                            "type": "DepsBash",
                            "short_name": "covalent",
                            "attributes": {
                                "commands": [],
                                "apply_fn": {
                                    "type": "TransportableObject",
                                    "attributes": {
                                        "_object": "{random_text}",
                                        "python_version": "3.8.10",
                                        "object_string": "<function apply_bash_commands at 0x7fcc59d0b040>",
                                        "_json": "",
                                        "attrs": {"doc": None, "name": "apply_bash_commands"},
                                    },
                                },
                                "apply_args": {
                                    "type": "TransportableObject",
                                    "attributes": {
                                        "_object": "gAWVBgAAAAAAAABdlF2UYS4=",
                                        "python_version": "3.8.10",
                                        "object_string": "[[]]",
                                        "_json": "[[]]",
                                        "attrs": {
                                            "doc": "Built-in mutable sequence.\n\nIf no argument is given, the constructor creates a new empty list.\nThe argument must be an iterable if specified.",
                                            "name": "",
                                        },
                                    },
                                },
                                "apply_kwargs": {
                                    "type": "TransportableObject",
                                    "attributes": {
                                        "_object": "gAV9lC4=",
                                        "python_version": "3.8.10",
                                        "object_string": "{}",
                                        "_json": "{}",
                                        "attrs": {
                                            "doc": "dict() -> new empty dictionary\ndict(mapping) -> new dictionary initialized from a mapping object's\n    (key, value) pairs\ndict(iterable) -> new dictionary initialized as if via:\n    d = {}\n    for k, v in iterable:\n        d[k] = v\ndict(**kwargs) -> new dictionary initialized with the name=value pairs\n    in the keyword argument list.  For example:  dict(one=1, two=2)",
                                            "name": "",
                                        },
                                    },
                                },
                                "retval_keyword": "",
                            },
                        }
                    },
                },
                {"file_name": "executor_data.pkl", "data": {}},
                {
                    "file_name": "function_string.txt",
                    "data": """@ct.electron\ndef hello(): return "Hello "\n"
                    """,
                },
                {
                    "file_name": "function.pkl",
                    "data": TransportableObject.make_transportable(
                        "<function hello at 0x7fcc2cdb4670>"
                    ),
                },
                {"file_name": "info.log", "data": ""},
                {
                    "file_name": "results.pkl",
                    "data": TransportableObject.make_transportable("Hello shore  !!"),
                },
                {"file_name": "stderr.log", "data": ""},
                {
                    "file_name": "stdout.log",
                    "data": """DEBUG: update_electrons_data called on node 5
DEBUG: update_electrons_data called on node 1""",
                },
                {"file_name": "value.pkl", "data": None},
            ],
        },
        "electron_files_node_1": {
            "path": "tests/covalent_ui_backend_tests/utils/mock_files/78525234-72ec-42dc-94a0-f4751707f9cd/node_1",
            "files": [
                {"file_name": "call_after.pkl", "data": []},
                {"file_name": "call_before.pkl", "data": []},
                {
                    "file_name": "deps.pkl",
                    "data": {
                        "bash": {
                            "type": "DepsBash",
                            "short_name": "covalent",
                            "attributes": {
                                "commands": [],
                                "apply_fn": {
                                    "type": "TransportableObject",
                                    "attributes": {
                                        "_object": "{random_text}",
                                        "python_version": "3.8.10",
                                        "object_string": "<function apply_bash_commands at 0x7fcc59d0b040>",
                                        "_json": "",
                                        "attrs": {"doc": None, "name": "apply_bash_commands"},
                                    },
                                },
                                "apply_args": {
                                    "type": "TransportableObject",
                                    "attributes": {
                                        "_object": "gAWVBgAAAAAAAABdlF2UYS4=",
                                        "python_version": "3.8.10",
                                        "object_string": "[[]]",
                                        "_json": "[[]]",
                                        "attrs": {
                                            "doc": "Built-in mutable sequence.\n\nIf no argument is given, the constructor creates a new empty list.\nThe argument must be an iterable if specified.",
                                            "name": "",
                                        },
                                    },
                                },
                                "apply_kwargs": {
                                    "type": "TransportableObject",
                                    "attributes": {
                                        "_object": "gAV9lC4=",
                                        "python_version": "3.8.10",
                                        "object_string": "{}",
                                        "_json": "{}",
                                        "attrs": {
                                            "doc": "dict() -> new empty dictionary\ndict(mapping) -> new dictionary initialized from a mapping object's\n    (key, value) pairs\ndict(iterable) -> new dictionary initialized as if via:\n    d = {}\n    for k, v in iterable:\n        d[k] = v\ndict(**kwargs) -> new dictionary initialized with the name=value pairs\n    in the keyword argument list.  For example:  dict(one=1, two=2)",
                                            "name": "",
                                        },
                                    },
                                },
                                "retval_keyword": "",
                            },
                        }
                    },
                },
                {"file_name": "executor_data.pkl", "data": {}},
                {
                    "file_name": "function_string.txt",
                    "data": """@ct.electron\ndef hello(): return "Hello "\n""",
                },
                {
                    "file_name": "function.pkl",
                    "data": TransportableObject.make_transportable(
                        "<function hello at 0x7fcc2cdb4670>"
                    ),
                },
                {"file_name": "info.log", "data": ""},
                {
                    "file_name": "results.pkl",
                    "data": TransportableObject.make_transportable("Hello shore  !!"),
                },
                {"file_name": "stderr.log", "data": ""},
                {"file_name": "stdout.log", "data": ""},
                {"file_name": "value.pkl", "data": None},
            ],
        },
        "electron_files_node_2": {
            "path": "tests/covalent_ui_backend_tests/utils/mock_files/78525234-72ec-42dc-94a0-f4751707f9cd/node_2",
            "files": [
                {"file_name": "call_after.pkl", "data": []},
                {"file_name": "call_before.pkl", "data": []},
                {
                    "file_name": "deps.pkl",
                    "data": {
                        "bash": {
                            "type": "DepsBash",
                            "short_name": "covalent",
                            "attributes": {
                                "commands": [],
                                "apply_fn": {
                                    "type": "TransportableObject",
                                    "attributes": {
                                        "_object": "{random_text}",
                                        "python_version": "3.8.10",
                                        "object_string": "<function apply_bash_commands at 0x7fcc59d0b040>",
                                        "_json": "",
                                        "attrs": {"doc": None, "name": "apply_bash_commands"},
                                    },
                                },
                                "apply_args": {
                                    "type": "TransportableObject",
                                    "attributes": {
                                        "_object": "gAWVBgAAAAAAAABdlF2UYS4=",
                                        "python_version": "3.8.10",
                                        "object_string": "[[]]",
                                        "_json": "[[]]",
                                        "attrs": {
                                            "doc": "Built-in mutable sequence.\n\nIf no argument is given, the constructor creates a new empty list.\nThe argument must be an iterable if specified.",
                                            "name": "",
                                        },
                                    },
                                },
                                "apply_kwargs": {
                                    "type": "TransportableObject",
                                    "attributes": {
                                        "_object": "gAV9lC4=",
                                        "python_version": "3.8.10",
                                        "object_string": "{}",
                                        "_json": "{}",
                                        "attrs": {
                                            "doc": "dict() -> new empty dictionary\ndict(mapping) -> new dictionary initialized from a mapping object's\n    (key, value) pairs\ndict(iterable) -> new dictionary initialized as if via:\n    d = {}\n    for k, v in iterable:\n        d[k] = v\ndict(**kwargs) -> new dictionary initialized with the name=value pairs\n    in the keyword argument list.  For example:  dict(one=1, two=2)",
                                            "name": "",
                                        },
                                    },
                                },
                                "retval_keyword": "",
                            },
                        }
                    },
                },
                {"file_name": "executor_data.pkl", "data": {}},
                {
                    "file_name": "function_string.txt",
                    "data": """@ct.electron\ndef hello(): return "Hello "\n""",
                },
                {
                    "file_name": "function.pkl",
                    "data": TransportableObject.make_transportable(
                        "<function hello at 0x7fcc2cdb4670>"
                    ),
                },
                {"file_name": "info.log", "data": ""},
                {
                    "file_name": "results.pkl",
                    "data": TransportableObject.make_transportable("Hello shore  !!"),
                },
                {"file_name": "stderr.log", "data": ""},
                {"file_name": "stdout.log", "data": ""},
                {"file_name": "value.pkl", "data": None},
            ],
        },
        "electron_files_node_3": {
            "path": "tests/covalent_ui_backend_tests/utils/mock_files/78525234-72ec-42dc-94a0-f4751707f9cd/node_3",
            "files": [
                {"file_name": "call_after.pkl", "data": []},
                {"file_name": "call_before.pkl", "data": []},
                {
                    "file_name": "deps.pkl",
                    "data": {
                        "bash": {
                            "type": "DepsBash",
                            "short_name": "covalent",
                            "attributes": {
                                "commands": [],
                                "apply_fn": {
                                    "type": "TransportableObject",
                                    "attributes": {
                                        "_object": "{random_text}",
                                        "python_version": "3.8.10",
                                        "object_string": "<function apply_bash_commands at 0x7fcc59d0b040>",
                                        "_json": "",
                                        "attrs": {"doc": None, "name": "apply_bash_commands"},
                                    },
                                },
                                "apply_args": {
                                    "type": "TransportableObject",
                                    "attributes": {
                                        "_object": "gAWVBgAAAAAAAABdlF2UYS4=",
                                        "python_version": "3.8.10",
                                        "object_string": "[[]]",
                                        "_json": "[[]]",
                                        "attrs": {
                                            "doc": "Built-in mutable sequence.\n\nIf no argument is given, the constructor creates a new empty list.\nThe argument must be an iterable if specified.",
                                            "name": "",
                                        },
                                    },
                                },
                                "apply_kwargs": {
                                    "type": "TransportableObject",
                                    "attributes": {
                                        "_object": "gAV9lC4=",
                                        "python_version": "3.8.10",
                                        "object_string": "{}",
                                        "_json": "{}",
                                        "attrs": {
                                            "doc": "dict() -> new empty dictionary\ndict(mapping) -> new dictionary initialized from a mapping object's\n    (key, value) pairs\ndict(iterable) -> new dictionary initialized as if via:\n    d = {}\n    for k, v in iterable:\n        d[k] = v\ndict(**kwargs) -> new dictionary initialized with the name=value pairs\n    in the keyword argument list.  For example:  dict(one=1, two=2)",
                                            "name": "",
                                        },
                                    },
                                },
                                "retval_keyword": "",
                            },
                        }
                    },
                },
                {"file_name": "executor_data.pkl", "data": {}},
                {
                    "file_name": "function_string.txt",
                    "data": """@ct.electron\ndef hello(): return "Hello "\n""",
                },
                {
                    "file_name": "function.pkl",
                    "data": TransportableObject.make_transportable(
                        "<function hello at 0x7fcc2cdb4670>"
                    ),
                },
                {"file_name": "info.log", "data": ""},
                {
                    "file_name": "results.pkl",
                    "data": TransportableObject.make_transportable("Hello shore  !!"),
                },
                {"file_name": "stderr.log", "data": ""},
                {"file_name": "stdout.log", "data": ""},
                {"file_name": "value.pkl", "data": None},
            ],
        },
        "electron_files_node_4": {
            "path": "tests/covalent_ui_backend_tests/utils/mock_files/78525234-72ec-42dc-94a0-f4751707f9cd/node_4",
            "files": [
                {"file_name": "call_after.pkl", "data": []},
                {"file_name": "call_before.pkl", "data": []},
                {
                    "file_name": "deps.pkl",
                    "data": {
                        "bash": {
                            "type": "DepsBash",
                            "short_name": "covalent",
                            "attributes": {
                                "commands": [],
                                "apply_fn": {
                                    "type": "TransportableObject",
                                    "attributes": {
                                        "_object": "{random_text}",
                                        "python_version": "3.8.10",
                                        "object_string": "<function apply_bash_commands at 0x7fcc59d0b040>",
                                        "_json": "",
                                        "attrs": {"doc": None, "name": "apply_bash_commands"},
                                    },
                                },
                                "apply_args": {
                                    "type": "TransportableObject",
                                    "attributes": {
                                        "_object": "gAWVBgAAAAAAAABdlF2UYS4=",
                                        "python_version": "3.8.10",
                                        "object_string": "[[]]",
                                        "_json": "[[]]",
                                        "attrs": {
                                            "doc": "Built-in mutable sequence.\n\nIf no argument is given, the constructor creates a new empty list.\nThe argument must be an iterable if specified.",
                                            "name": "",
                                        },
                                    },
                                },
                                "apply_kwargs": {
                                    "type": "TransportableObject",
                                    "attributes": {
                                        "_object": "gAV9lC4=",
                                        "python_version": "3.8.10",
                                        "object_string": "{}",
                                        "_json": "{}",
                                        "attrs": {
                                            "doc": "dict() -> new empty dictionary\ndict(mapping) -> new dictionary initialized from a mapping object's\n    (key, value) pairs\ndict(iterable) -> new dictionary initialized as if via:\n    d = {}\n    for k, v in iterable:\n        d[k] = v\ndict(**kwargs) -> new dictionary initialized with the name=value pairs\n    in the keyword argument list.  For example:  dict(one=1, two=2)",
                                            "name": "",
                                        },
                                    },
                                },
                                "retval_keyword": "",
                            },
                        }
                    },
                },
                {"file_name": "executor_data.pkl", "data": {}},
                {
                    "file_name": "function_string.txt",
                    "data": """@ct.electron\ndef hello(): return "Hello "\n""",
                },
                {
                    "file_name": "function.pkl",
                    "data": TransportableObject.make_transportable(
                        "<function hello at 0x7fcc2cdb4670>"
                    ),
                },
                {"file_name": "info.log", "data": ""},
                {
                    "file_name": "results.pkl",
                    "data": TransportableObject.make_transportable("Hello shore  !!"),
                },
                {"file_name": "stderr.log", "data": ""},
                {"file_name": "stdout.log", "data": ""},
                {"file_name": "value.pkl", "data": None},
            ],
        },
        "electron_files_node_5": {
            "path": "tests/covalent_ui_backend_tests/utils/mock_files/78525234-72ec-42dc-94a0-f4751707f9cd/node_5",
            "files": [
                {"file_name": "call_after.pkl", "data": []},
                {"file_name": "call_before.pkl", "data": []},
                {
                    "file_name": "deps.pkl",
                    "data": {
                        "bash": {
                            "type": "DepsBash",
                            "short_name": "covalent",
                            "attributes": {
                                "commands": [],
                                "apply_fn": {
                                    "type": "TransportableObject",
                                    "attributes": {
                                        "_object": "{random_text}",
                                        "python_version": "3.8.10",
                                        "object_string": "<function apply_bash_commands at 0x7fcc59d0b040>",
                                        "_json": "",
                                        "attrs": {"doc": None, "name": "apply_bash_commands"},
                                    },
                                },
                                "apply_args": {
                                    "type": "TransportableObject",
                                    "attributes": {
                                        "_object": "gAWVBgAAAAAAAABdlF2UYS4=",
                                        "python_version": "3.8.10",
                                        "object_string": "[[]]",
                                        "_json": "[[]]",
                                        "attrs": {
                                            "doc": "Built-in mutable sequence.\n\nIf no argument is given, the constructor creates a new empty list.\nThe argument must be an iterable if specified.",
                                            "name": "",
                                        },
                                    },
                                },
                                "apply_kwargs": {
                                    "type": "TransportableObject",
                                    "attributes": {
                                        "_object": "gAV9lC4=",
                                        "python_version": "3.8.10",
                                        "object_string": "{}",
                                        "_json": "{}",
                                        "attrs": {
                                            "doc": "dict() -> new empty dictionary\ndict(mapping) -> new dictionary initialized from a mapping object's\n    (key, value) pairs\ndict(iterable) -> new dictionary initialized as if via:\n    d = {}\n    for k, v in iterable:\n        d[k] = v\ndict(**kwargs) -> new dictionary initialized with the name=value pairs\n    in the keyword argument list.  For example:  dict(one=1, two=2)",
                                            "name": "",
                                        },
                                    },
                                },
                                "retval_keyword": "",
                            },
                        }
                    },
                },
                {"file_name": "executor_data.pkl", "data": {}},
                {
                    "file_name": "function_string.txt",
                    "data": """@ct.electron\ndef hello(): return "Hello "\n""",
                },
                {
                    "file_name": "function.pkl",
                    "data": TransportableObject.make_transportable(
                        "<function hello at 0x7fcc2cdb4670>"
                    ),
                },
                {"file_name": "info.log", "data": ""},
                {
                    "file_name": "results.pkl",
                    "data": TransportableObject.make_transportable("Hello shore  !!"),
                },
                {"file_name": "stderr.log", "data": ""},
                {"file_name": "stdout.log", "data": ""},
                {"file_name": "value.pkl", "data": None},
            ],
        },
        "log_files": {
            "path": "tests/covalent_ui_backend_tests/utils/mock_files/log_files",
            "files": [
                {
                    "file_name": "case_1.log",
                    "data": """[2022-09-23 07:43:59,752] [INFO] Started server process [41482]
[2022-09-23 07:43:59,753] [INFO] Waiting for application startup.
[2022-09-23 07:43:59,753] [INFO] Application startup complete.
[2022-09-26 07:41:42,411] [INFO] 127.0.0.1:47378 - "GET /docs HTTP/1.1" 200
[2022-09-26 07:41:42,907] [INFO] 127.0.0.1:47378 - "GET /openapi.json HTTP/1.1" 200""",
                },
                {
                    "file_name": "case_2.log",
                    "data": """[2022-09-23 07:43:59,752] [INFO] Started server process [41482]
[2022-09-23 07:43:59,753] [INFO] Waiting for application startup.
[2022-09-23 07:43:59,753] [INFO] Application startup complete.
[2022-09-26 07:41:42,411] [INFO] 127.0.0.1:47378 - "GET /docs HTTP/1.1" 200
[2022-09-26 07:41:42,907] [INFO] 127.0.0.1:47378 - "GET /openapi.json HTTP/1.1" 200
connection Closed
Killed
[2022-09-26 07:41:42,907] [INFO] WebSocket - connection open
[2022-09-26 07:41:42,907] [INFO] 127.0.0.1:47378 - "GET /favicon.ico HTTP/1.1" 404""",
                },
                {
                    "file_name": "case_3.log",
                    "data": """Killed
[2022-09-23 07:43:59,752] [INFO] Started server process [41482]
[2022-09-23 07:43:59,753] [INFO] Waiting for application startup.
[2022-09-23 07:43:59,753] [INFO] Application startup complete.
[2022-09-26 07:41:42,411] [INFO] 127.0.0.1:47378 - "GET /docs HTTP/1.1" 200
[2022-09-26 07:41:42,907] [INFO] 127.0.0.1:47378 - "GET /openapi.json HTTP/1.1" 200
connection Closed
[2022-09-26 07:41:42,907] [INFO] WebSocket - connection open
[2022-09-26 07:41:42,907] [INFO] 127.0.0.1:47378 - "GET /favicon.ico HTTP/1.1" 404
Connection Closed
killed""",
                },
            ],
        },
    }
