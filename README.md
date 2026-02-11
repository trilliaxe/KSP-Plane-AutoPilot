# KSP Plane AutoPilot

**KSP Plane AutoPilot** is a Python-based autopilot controller for atmospheric and powered flight in *Kerbal Space Program* using the kRPC interface.  
It allows you to automate flight control of aircraft and spaceplanes from takeoff through cruise and landing phases with code-driven logic.

This project requires a running instance of Kerbal Space Program and the kRPC mod.

##  Features

- Python-controlled autopilot for **Kerbal Space Program** aircraft and spaceplanes  
- Connects to KSP via **kRPC** to read vessel state and send control commands  
- Supports basic flight automation: **heading**, **altitude**, **airspeed**, and attitude control  
- Designed to be extensible for custom flight logic and strategies

##  Requirements

Before using this autopilot, make sure you have the following installed:

1. **Kerbal Space Program** with the kRPC mod enabled  
2. Python 3.8+  
3. Python dependencies (see below)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/trilliaxe/KSP-Plane-AutoPilot.git
   cd KSP-Plane-AutoPilot
2. Create and activate your Python virtual environment:
   ```bash
   python -m venv pyvenv
3. Activate your environment
   ```bash
   .pyvenv\Scripts\activate
4. Launch the autopilot:
   ```bash
   python <Program.py>
