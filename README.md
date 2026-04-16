# TRNSYS-AgentControl

TRNSYS-AgentControl is a Python-based workflow for agent-driven supervisory control studies with TRNSYS. The current implementation supports control-environment construction, agent training, and runtime inference through the TRNSYS Python interface.

The workflow is designed to stay application-configurable. Users can define project-specific states, actions, rewards, and control constraints according to their own TRNSYS model. In the present example, a DQN-based agent is used for demonstration, but the general workflow can be adapted to other Python-based decision agents.

## Current scope

This repository does **not** automatically modify or build TRNSYS models.

The intended workflow is:

1. Export or prepare a training-ready dataset from TRNSYS-based simulation results.
2. Train the control agent in Python.
3. Export the trained policy for deployment.
4. Manually place the runtime script and trained model into the TRNSYS Python connector workflow.

This design keeps the framework independent from legacy or project-specific TRNSYS file structures while preserving closed-loop deployment capability.

## Repository structure

```text
trnsys_agent_control/
│
├── src/
│   ├── baseline_processor.py
│   ├── env.py
│   ├── trainer.py
│   ├── runtime_agent.py
│   └── utils.py
│
├── examples/
│   └── pv_battery_case/
│       ├── Meta_data_RuleBased_Result.xlsx
│       ├── best_model.zip
│       └── trnsys_runtime_example.py
│
├── README.md
├── requirements.txt
└── LICENSE.txt

Main components

baseline_processor.py
Provides an example preprocessing utility for generating a rule-based comparison dataset when needed. This step is not required for the illustrative training workflow included in the present repository.

env.py
Defines the control environment, including state construction, action space, transition logic, and reward calculation.

trainer.py
Handles agent training, evaluation, logging, and model export.

runtime_agent.py
Loads the trained model, receives real-time state inputs from the TRNSYS Python connector, performs inference, maps the selected action to a control signal, and returns outputs to TRNSYS.

utils.py
Contains shared helper functions for data handling and repeated utility operations.

Example case
The repository currently includes one illustrative example based on a building-scale PV-battery energy management case.

Example files:
Meta_data_RuleBased_Result.xlsx: training-ready dataset used in the illustrative example
best_model.zip: example trained model
trnsys_runtime_example.py: example runtime deployment script for TRNSYS

Installation
Create a Python environment and install the required packages:

pip install -r requirements.txt

Dependencies

Typical dependencies include:
pandas
numpy
openpyxl
gymnasium
stable-baselines3
matplotlib

Additional packages may be required depending on the selected agent backend.

Basic workflow

1. Train the agent
Run the training script using the provided example dataset:

python src/trainer.py

Input:
Meta_data_RuleBased_Result.xlsx

Typical outputs:
trained model
evaluation logs
training logs
monitoring files

2. Deploy in TRNSYS
Use the trained model together with the runtime script in the TRNSYS Python connector.

At runtime, TRNSYS provides the selected input states to Python, the agent predicts the control action, and the returned output is written back to the TRNSYS model.

Notes on flexibility

The framework is intended to be configurable at the application level.

The following elements may vary from one project to another:

selected state variables
action definition
reward formulation
penalty terms
operational limits
fallback or baseline logic

The current example demonstrates the workflow with a specific case study and a specific trained agent, but the overall structure can be adapted to other supervisory control problems implemented on the Python side.

Current limitations
TRNSYS data export is manual.
Reintegration into the TRNSYS Python connector is manual.
The current repository includes one example case.
The present example demonstrates one agent implementation and should not be interpreted as a restriction of the general workflow to a single algorithm.

Intended use
This repository is intended for researchers and engineers who want to build and test Python-based supervisory control agents around TRNSYS simulation outputs and deploy trained decision logic back into TRNSYS through the available Python interface.

Citation
Citation information will be added after manuscript finalization.

License
See LICENSE.txt