# Copyright 2021 Agnostiq Inc.
#
# This file is part of Covalent.
#
# Licensed under the Apache License 2.0 (the "License"). A copy of the
# License may be obtained with this software package or at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Use of this file is prohibited except in compliance with the License.
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Functions to convert tg -> TransportGraphSchema"""

import os
from pathlib import Path
from typing import List

import networkx as nx

from .._shared_files.schemas.edge import EdgeMetadata, EdgeSchema
from .._shared_files.schemas.electron import ElectronSchema
from .._shared_files.schemas.transport_graph import TransportGraphSchema
from .._workflow.transport import _TransportGraph
from .electron import deserialize_node, serialize_node


def serialize_edge(source: int, target: int, attrs: dict) -> EdgeSchema:
    meta = EdgeMetadata(
        edge_name=attrs["edge_name"],
        param_type=attrs.get("param_type"),
        arg_index=attrs.get("arg_index"),
    )
    return EdgeSchema(source=source, target=target, metadata=meta)


def deserialize_edge(e: EdgeSchema) -> dict:
    return {
        "source": e.source,
        "target": e.target,
        "attrs": e.metadata.dict(),
    }


def _serialize_nodes(g: nx.MultiDiGraph, storage_path: str) -> List[ElectronSchema]:
    results = []
    base_path = Path(storage_path)
    for i in g.nodes:
        node_storage_path = base_path / f"node_{i}"
        os.mkdir(node_storage_path)
        results.append(serialize_node(i, g.nodes[i], node_storage_path))
    return results


def _serialize_edges(g: nx.MultiDiGraph) -> List[EdgeSchema]:
    results = []
    for edge in g.edges:
        source, target, key = edge
        results.append(serialize_edge(source, target, g.edges[edge]))
    return results


def serialize_transport_graph(tg, storage_path: str) -> TransportGraphSchema:
    g = tg.get_internal_graph_copy()
    return TransportGraphSchema(
        nodes=_serialize_nodes(g, storage_path),
        links=_serialize_edges(g),
    )


def deserialize_transport_graph(t: TransportGraphSchema) -> _TransportGraph:
    tg = _TransportGraph()
    g = tg._graph
    nodes = [deserialize_node(n) for n in t.nodes]
    edges = [deserialize_edge(e) for e in t.links]
    for node in nodes:
        node_id = node["id"]
        attrs = node["attrs"]
        g.add_node(node_id, **attrs)
    for edge in edges:
        x = edge["source"]
        y = edge["target"]
        g.add_edge(x, y, **edge["attrs"])

    return tg
