# -*- coding: utf-8 -*-

# (C) Copyright 2023 IBM. All Rights Reserved.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

from dataclasses import dataclass
import logging
import networkx as nx
from networkx.exception import NetworkXError

# from ai_synthesis_py import LinFuncSynthesis  # RUST
from qiskit_ibm_transpiler.ai.rl_inferences.linear_functions import (
    RLInferenceLinFuncRust,
)

from typing import Union, List

import numpy as np
from qiskit import QuantumCircuit
from qiskit.transpiler import CouplingMap
from qiskit.circuit.library import LinearFunction
from qiskit.quantum_info import Clifford
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit_ibm_transpiler.ai.models.linear_functions import (
    MODEL_CMAPS as MODEL_LIN_FUNC_CMAPS,
    MODEL_HASHES as MODEL_LIN_FUNC_HASHES,
)
from qiskit_ibm_transpiler.utils import get_qasm_from_circuit

logger = logging.getLogger(__name__)


# class AICliffordAPI(QiskitTranspilerService):
#     """A helper class that covers some basic funcionality from the Clifford AI Synthesis API"""

#     def __init__(self, **kwargs):
#         super().__init__(path_param="clifford", **kwargs)

#     def transpile(
#         self,
#         circuits: List[Union[QuantumCircuit, Clifford]],
#         qargs: List[List[int]],
#         coupling_map: Union[List[List[int]], None] = None,
#         backend_name: Union[str, None] = None,
#     ):
#         if coupling_map is not None:
#             transpile_resps = self.request_and_wait(
#                 endpoint="transpile",
#                 body={
#                     "clifford_dict": [
#                         Clifford(circuit).to_dict() for circuit in circuits
#                     ],
#                     "qargs": qargs,
#                     "backend_coupling_map": coupling_map,
#                 },
#                 params=dict(),
#             )
#         elif backend_name is not None:
#             transpile_resps = self.request_and_wait(
#                 endpoint="transpile",
#                 body={
#                     "clifford_dict": [
#                         Clifford(circuit).to_dict() for circuit in circuits
#                     ],
#                     "qargs": qargs,
#                 },
#                 params={"backend": backend_name},
#             )
#         else:
#             raise (
#                 f"ERROR. Either a 'coupling_map' or a 'backend_name' must be provided."
#             )

#         results = []
#         for transpile_resp in transpile_resps:
#             if transpile_resp.get("success") and transpile_resp.get("qasm") is not None:
#                 results.append(QuantumCircuit.from_qasm_str(transpile_resp.get("qasm")))
#             else:
#                 results.append(None)
#         return results


class AILocalLinearFunctionSynthesis:
    """A helper class that covers some basic funcionality from the Linear Function AI Local Synthesis"""

    def transpile(
        self,
        circuits: List[Union[QuantumCircuit, LinearFunction]],
        qargs: List[List[int]],
        coupling_map: Union[List[List[int]], None] = None,
        backend_name: Union[str, None] = None,
    ) -> List[Union[QuantumCircuit, None]]:
        """Synthetize one or more quantum circuits into an optimized equivalent. It differs from a standard synthesis process in that it takes into account where the linear functions are (qargs)
        and respects it on the synthetized circuit.

        Args:
            circuits (List[Union[QuantumCircuit, LinearFunction]]): A list of quantum circuits to be synthetized.
            qargs (List[List[int]]): A list of lists of qubit indices for each circuit. Each list of qubits indices represent where the linear function circuit is.
            coupling_map (Union[List[List[int]], None]): A coupling map representing the connectivity of the quantum computer.
            backend_name (Union[str, None]): The name of the backend to use for the synthesis.

        Returns:
            List[Union[QuantumCircuit, None]]: A list of synthetized quantum circuits. If the synthesis fails for any circuit, the corresponding element in the list will be None.
        """

        # Although this function is called `transpile`, it does a synthesis. It has this name because the synthesis
        # is made as a pass on the Qiskit Pass Manager which is used in the transpilation process.

        if not coupling_map and not backend_name:
            raise ValueError(
                f"ERROR. Either a 'coupling_map' or a 'backend_name' must be provided."
            )

        n_circs = len(circuits)
        n_qargs = len(qargs)

        if n_circs != n_qargs:
            raise ValueError(
                f"ERROR. The number of input circuits {n_circs}"
                f"and the number of input qargs arrays {n_qargs} are different."
            )

        clifford_dict = [Clifford(circuit).to_dict() for circuit in circuits]

        coupling_map_graph = get_coupling_map(backend_name, coupling_map)

        transpile_response = launch_transpile_task(
            coupling_map_graph, clifford_dict, qargs
        )

        synthetized_circuits = []
        for response_element in transpile_response:
            synthetized_circuit = None
            if response_element.success and response_element.qasm:
                synthetized_circuit = QuantumCircuit.from_qasm_str(
                    response_element.qasm
                )
            synthetized_circuits.append(synthetized_circuit)

        return synthetized_circuits


# class AIPermutationAPI(QiskitTranspilerService):
#     """A helper class that covers some basic funcionality from the Permutation AI Synthesis API"""

#     def __init__(self, **kwargs):
#         super().__init__(path_param="permutations", **kwargs)

#     def transpile(
#         self,
#         patterns: List[List[int]],
#         qargs: List[List[int]],
#         coupling_map: Union[List[List[int]], None] = None,
#         backend_name: Union[str, None] = None,
#     ):

#         if coupling_map is not None:
#             transpile_resps = self.request_and_wait(
#                 endpoint="transpile",
#                 body={
#                     "permutation": patterns,
#                     "qargs": qargs,
#                     "backend_coupling_map": coupling_map,
#                 },
#                 params=dict(),
#             )
#         elif backend_name is not None:
#             transpile_resps = self.request_and_wait(
#                 endpoint="transpile",
#                 body={
#                     "permutation": patterns,
#                     "qargs": qargs,
#                 },
#                 params={"backend": backend_name},
#             )
#         else:
#             raise (
#                 f"ERROR. Either a 'coupling_map' or a 'backend_name' must be provided."
#             )

#         results = []
#         for transpile_resp in transpile_resps:
#             if transpile_resp.get("success") and transpile_resp.get("qasm") is not None:
#                 results.append(QuantumCircuit.from_qasm_str(transpile_resp.get("qasm")))
#             else:
#                 results.append(None)
#         return results


def perm_cliff(cliff, perm):
    perm = np.array(perm)
    cliff.stab_x = cliff.stab_x[:, perm]
    cliff.stab_z = cliff.stab_z[:, perm]
    cliff.destab_x = cliff.destab_x[:, perm]
    cliff.destab_z = cliff.destab_z[:, perm]
    cliff.stab = cliff.stab[perm, :]
    cliff.destab = cliff.destab[perm, :]
    return cliff


@dataclass
class LayoutResult:
    """Enum for layout result"""

    initial: List[int]
    final: List[int]


@dataclass
class RlResult:
    """Enum for Rl Result information"""

    qasm: str | None = None
    success: bool = False
    layout: LayoutResult | None = None
    error: str | None = None


def launch_transpile_task(
    coupling_map: nx.Graph, clifford_dict, circuits_qubits_indexes: List[List[int]]
):
    transpile_response = []

    for index, circuit_qubits_indexes in enumerate(circuits_qubits_indexes):
        subgraph_perm, cmap_hash = get_subgraph_model_rust(
            coupling_map=coupling_map,
            qargs=circuit_qubits_indexes,
        )

        # Make sure I should use index here
        clifford = perm_cliff(Clifford.from_dict(clifford_dict[index]), subgraph_perm)

        # Generate the Clifford from the dictionary to send it to the model and permute it
        # Synth the input
        rl_circuit = RLInferenceLinFuncRust().synthesize(
            cliff=clifford, coupling_map_hash=cmap_hash
        )
        # Permute the circuit back
        rl_circuit = QuantumCircuit(rl_circuit.num_qubits).compose(
            rl_circuit, qubits=subgraph_perm
        )

        rl_result = RlResult(
            qasm=get_qasm_from_circuit(rl_circuit),
            success=False if rl_circuit is None else True,
        )

        transpile_response.append(rl_result)

    return transpile_response


def get_coupling_map(
    backend_name: str | None = None, backend_coupling_map: list[list[int]] | None = None
) -> nx.Graph:
    coupling_map_list_format = None

    if backend_coupling_map:
        coupling_map_list_format = backend_coupling_map
    elif backend_name:
        try:
            runtime_service = QiskitRuntimeService()
            backend_info = runtime_service.backend(name=backend_name)
            coupling_map_edges = CouplingMap.get_edges(backend_info.coupling_map)
            coupling_map_list_format = [list(edge) for edge in coupling_map_edges]
        except Exception:
            raise PermissionError(f"ERROR. Backend not supported ({backend_name})")

    try:
        coupling_map = nx.Graph(coupling_map_list_format)
    except Exception:
        raise NetworkXError(f"ERROR. Cannot convert coupling_map from list to graph")

    return coupling_map


def get_mapping_perm(coupling_map: nx.Graph, circuit_qubits_indexes: List[int]):
    model_coupling_map_by_model_hash = {
        model_hash: model_coupling_map
        for model_hash, model_coupling_map in zip(
            MODEL_LIN_FUNC_HASHES, MODEL_LIN_FUNC_CMAPS
        )
    }

    # Identify the subgraph of the coupling map where the circuit is.
    circuit_in_coupling_map = coupling_map.subgraph(circuit_qubits_indexes)

    # Check if it is connected
    if not nx.is_connected(circuit_in_coupling_map):
        return None, None, False

    # We find which model to use by hashing the input graph
    circuit_in_coupling_map_hash = nx.weisfeiler_lehman_graph_hash(
        circuit_in_coupling_map
    )

    # If there is no model for that circuit_in_coupling_map, we cannot use AI.
    if circuit_in_coupling_map_hash not in model_coupling_map_by_model_hash:
        return None, None, True

    model_coupling_map = model_coupling_map_by_model_hash[circuit_in_coupling_map_hash]
    # Maps the circuit_in_coupling_map and the model's topology
    cmap_to_model = next(
        iter(
            nx.isomorphism.GraphMatcher(
                circuit_in_coupling_map, nx.Graph(model_coupling_map)
            ).match()
        )
    )

    # We now have to find the permutation that we should apply to the Clifford based on the mapping we found
    qargs_dict = {v: i for i, v in enumerate(circuit_qubits_indexes)}
    subgraph_perm = [
        qargs_dict[v]
        for v in sorted(cmap_to_model.keys(), key=lambda k: cmap_to_model[k])
    ]

    return subgraph_perm, circuit_in_coupling_map_hash, True


def get_subgraph_model_rust(
    coupling_map: nx.Graph,
    qargs: list[int] | None = None,
):
    try:
        subgraph_perm, cmap_hash, is_connected = get_mapping_perm(coupling_map, qargs)
    except BaseException:
        raise AttributeError(f"ERROR. Malformed qargs {qargs}")

    if not is_connected:
        raise ValueError(
            "ERROR. Qargs do not form a connected subgraph of the backend coupling map"
        )

    if cmap_hash not in MODEL_LIN_FUNC_HASHES:
        raise LookupError(f"ERROR. No model available for the requested subgraph")

    return subgraph_perm, cmap_hash