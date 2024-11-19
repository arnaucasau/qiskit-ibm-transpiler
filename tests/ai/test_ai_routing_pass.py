# -*- coding: utf-8 -*-

# (C) Copyright 2024 IBM. All Rights Reserved.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Unit-testing routing_ai"""

import pytest
from qiskit import QuantumCircuit
from qiskit.transpiler import PassManager
from qiskit.transpiler.exceptions import TranspilerError

from qiskit_ibm_transpiler.ai.routing import AIRouting
from tests import brisbane_coupling_map, brisbane_coupling_map_list_format


@pytest.mark.skip(
    reason="Unreliable. It passes most of the times with the timeout of 1 second for the current circuits used"
)
def test_ai_cloud_routing_pass_exceed_timeout(qv_circ, brisbane_backend_name):
    ai_routing_pass = PassManager(
        [
            AIRouting(backend_name=brisbane_backend_name, timeout=1, local_mode=False),
        ]
    )
    ai_optimized_circuit = ai_routing_pass.run(qv_circ)
    assert isinstance(ai_optimized_circuit, QuantumCircuit)


def test_ai_cloud_routing_pass_wrong_token(qv_circ, brisbane_backend_name):
    ai_routing_pass = PassManager(
        [
            AIRouting(
                backend_name=brisbane_backend_name,
                token="invented_token_2",
                local_mode=False,
            ),
        ]
    )
    try:
        ai_optimized_circuit = ai_routing_pass.run(qv_circ)
        pytest.fail("Error expected")
    except Exception as e:
        assert "Invalid authentication credentials" in str(e)


@pytest.mark.disable_monkeypatch
def test_ai_cloud_routing_pass_wrong_url(qv_circ, brisbane_backend_name):
    ai_routing_pass = PassManager(
        [
            AIRouting(
                backend_name=brisbane_backend_name,
                base_url="https://ibm.com/",
                local_mode=False,
            ),
        ]
    )
    try:
        ai_optimized_circuit = ai_routing_pass.run(qv_circ)
        pytest.fail("Error expected")
    except Exception as e:
        assert "Internal error: 404 Client Error: Not Found for url" in str(e)
        assert type(e).__name__ == "TranspilerError"


@pytest.mark.disable_monkeypatch
def test_ai_cloud_routing_pass_unexisting_url(qv_circ, brisbane_backend_name):
    ai_routing_pass = PassManager(
        [
            AIRouting(
                backend_name=brisbane_backend_name,
                base_url="https://invented-domain-qiskit-ibm-transpiler-123.com/",
                local_mode=False,
            ),
        ]
    )
    try:
        ai_optimized_circuit = ai_routing_pass.run(qv_circ)
        pytest.fail("Error expected")
    except Exception as e:
        print(e)
        assert (
            "Error: HTTPSConnectionPool(host=\\'invented-domain-qiskit-ibm-transpiler-123.com\\', port=443):"
            in str(e)
        )
        assert type(e).__name__ == "TranspilerError"


@pytest.mark.parametrize(
    "local_mode, error_type",
    [(True, PermissionError), (False, TranspilerError)],
    ids=["local_mode", "cloud_mode"],
)
def test_ai_routing_pass_wrong_backend(
    error_type, local_mode, random_circuit_transpiled
):
    with pytest.raises(
        error_type,
        match=r"User doesn\'t have access to the specified backend: \w+",
    ):
        ai_routing_pass = PassManager(
            [
                AIRouting(backend_name="wrong_backend", local_mode=local_mode),
            ]
        )
        ai_routing_pass.run(random_circuit_transpiled)


@pytest.mark.parametrize("optimization_level", [0, 4])
@pytest.mark.parametrize(
    "local_mode",
    ["true", "false"],
    ids=["local_mode", "cloud_mode"],
)
def test_ai_routing_pass_wrong_opt_level(
    optimization_level, local_mode, brisbane_backend_name, qv_circ
):
    with pytest.raises(
        ValueError,
        match=r"ERROR. The optimization_level should be a value between 1 and 3.",
    ):
        ai_routing_pass = PassManager(
            [
                AIRouting(
                    optimization_level=optimization_level,
                    backend_name=brisbane_backend_name,
                    local_mode=local_mode,
                )
            ]
        )
        ai_routing_pass.run(qv_circ)


@pytest.mark.parametrize("optimization_level", [1, 2, 3])
@pytest.mark.parametrize(
    "local_mode",
    ["true", "false"],
    ids=["local_mode", "cloud_mode"],
)
def test_ai_routing_pass_valid_opt_level(
    optimization_level,
    local_mode,
    brisbane_backend_name,
    qv_circ,
):
    ai_routing_pass = PassManager(
        [
            AIRouting(
                optimization_level=optimization_level,
                backend_name=brisbane_backend_name,
                local_mode=local_mode,
            )
        ]
    )

    circuit = ai_routing_pass.run(qv_circ)

    assert isinstance(circuit, QuantumCircuit)


@pytest.mark.parametrize("optimization_preferences", ["foo"])
@pytest.mark.parametrize(
    "local_mode",
    ["true", "false"],
    ids=["local_mode", "cloud_mode"],
)
def test_ai_routing_pass_wrong_opt_preferences(
    optimization_preferences, local_mode, brisbane_backend_name, qv_circ
):
    with pytest.raises(
        ValueError,
        match=r"'\w+' is not a valid optimization preference",
    ):
        ai_routing_pass = PassManager(
            [
                AIRouting(
                    optimization_preferences=optimization_preferences,
                    backend_name=brisbane_backend_name,
                    local_mode=local_mode,
                )
            ]
        )
        ai_routing_pass.run(qv_circ)


@pytest.mark.parametrize(
    "optimization_preferences", [None, "noise", ["noise", "n_cnots"]]
)
@pytest.mark.parametrize(
    "local_mode",
    ["true", "false"],
    ids=["local_mode", "cloud_mode"],
)
def test_ai_routing_pass_valid_opt_preferences(
    optimization_preferences,
    local_mode,
    brisbane_backend_name,
    qv_circ,
):
    ai_routing_pass = PassManager(
        [
            AIRouting(
                backend_name=brisbane_backend_name,
                optimization_preferences=optimization_preferences,
                local_mode=local_mode,
            )
        ]
    )

    circuit = ai_routing_pass.run(qv_circ)

    assert isinstance(circuit, QuantumCircuit)


@pytest.mark.parametrize("layout_mode", ["RECREATE", "BOOST"])
@pytest.mark.parametrize(
    "local_mode",
    ["true", "false"],
    ids=["local_mode", "cloud_mode"],
)
def test_ai_routing_pass_wrong_layout_mode(
    layout_mode, local_mode, brisbane_backend_name
):
    with pytest.raises(ValueError):
        PassManager(
            [
                AIRouting(
                    layout_mode=layout_mode,
                    backend_name=brisbane_backend_name,
                    local_mode=local_mode,
                )
            ]
        )


@pytest.mark.parametrize("layout_mode", ["KEEP", "OPTIMIZE", "IMPROVE"])
@pytest.mark.parametrize(
    "local_mode",
    ["true", "false"],
    ids=["local_mode", "cloud_mode"],
)
def test_ai_routing_pass_valid_layout_mode(
    layout_mode,
    local_mode,
    brisbane_backend_name,
    qv_circ,
):
    ai_routing_pass = PassManager(
        [
            AIRouting(
                layout_mode=layout_mode,
                backend_name=brisbane_backend_name,
                local_mode=local_mode,
            )
        ]
    )

    circuit = ai_routing_pass.run(qv_circ)

    assert isinstance(circuit, QuantumCircuit)


@pytest.mark.parametrize(
    "local_mode",
    ["true", "false"],
    ids=["local_mode", "cloud_mode"],
)
def test_ai_routing_pass_with_backend_name(
    local_mode,
    brisbane_backend_name,
    qv_circ,
):
    ai_routing_pass = PassManager(
        [
            AIRouting(
                backend_name=brisbane_backend_name,
                local_mode=local_mode,
            )
        ]
    )

    circuit = ai_routing_pass.run(qv_circ)

    assert isinstance(circuit, QuantumCircuit)


@pytest.mark.parametrize(
    "local_mode",
    ["true", "false"],
    ids=["local_mode", "cloud_mode"],
)
def test_ai_routing_pass_with_backend(
    local_mode,
    brisbane_backend,
    qv_circ,
):
    ai_routing_pass = PassManager(
        [
            AIRouting(
                backend=brisbane_backend,
                local_mode=local_mode,
            )
        ]
    )

    circuit = ai_routing_pass.run(qv_circ)

    assert isinstance(circuit, QuantumCircuit)


@pytest.mark.parametrize(
    "coupling_map",
    [brisbane_coupling_map, brisbane_coupling_map_list_format],
    indirect=True,
    ids=["coupling_map_object", "coupling_map_list"],
)
@pytest.mark.parametrize(
    "local_mode",
    ["true", "false"],
    ids=["local_mode", "cloud_mode"],
)
def test_ai_routing_pass_with_coupling_map(
    coupling_map,
    local_mode,
    qv_circ,
):
    ai_routing_pass = PassManager(
        [
            AIRouting(
                coupling_map=coupling_map,
                local_mode=local_mode,
            )
        ]
    )

    circuit = ai_routing_pass.run(qv_circ)

    assert isinstance(circuit, QuantumCircuit)