# SyncOS Fleet Management & Orchestration Analysis

Welcome to the **SyncOS** fleet management and optimization analysis repository. This project evaluates operational bottlenecks in an automated warehouse facility, validates root-cause hypotheses using simulated telemetry data, and presents a data-driven engineering roadmap for SyncOS—an autonomous fleet orchestration engine.

---

## 📌 Executive Summary

SyncOS orchestrates a mixed fleet of 10 Autonomous Mobile Robots (AMRs) operating 24/7. By analyzing 7 days of operational telemetry across 5,000 completed tasks, key operational bottlenecks were identified in task dispatch, charging management, and traffic density. Implementing targeted orchestration updates (predictive charging, proximity routing, and zone corridors) yields up to a **+14.7% increase in total throughput**.

---

## 🤖 System & Fleet Overview

- **Operating Model**: Continuous 24/7 operation across 3 standard production shifts.
- **Fleet Composition**: Exactly 10 vehicles
  - **5 Autonomous Forklifts (`FL-01` to `FL-05`)**: Specialized for heavy pallet transport.
  - **5 Dual-Conveyor Robots (`CV-01` to `CV-05`)**: Specialized for intermediate material transfers.
- **Baseline Orchestration Engine**:
  - **Payload Compatibility**: Automated matching between task payload type and vehicle class.
  - **Dispatch Logic**: Strict First-In, First-Out (FIFO) chronological dispatching without geographic proximity weighting.
  - **Charging Logic**: Reactive "run-to-depletion" threshold (~24% battery).
  - **Real-time Capabilities**: Real-time X/Y spatial coordinate tracking and API authority to dynamically command or reassign fleet units.

---

## 📊 Telemetry Data Schema & Synthetic Generation Methodology

To conduct rigorous hypothesis testing without hardcoding expected outcomes, telemetry was generated using **procedural simulation** rather than uniform randomness.

### Data Generation Philosophy
- **Gaussian Distributions**: Task creation, pickup, and transit durations are modeled on normal (bell) curves reflecting physical machine variance and human handover delays.
- **Spatial Weighting**: Facility zones are weighted realistically (e.g., higher traffic concentration in `Dispatch_Zone` and `Aisle_1`).
- **Sequential State & Battery Tracking**: Batteries drain based on active movement state (`Moving_Loaded`, `Moving_Empty`) and recharge sequentially in `Charging_Bay`.
- **Temporal Curves**: Task generation rates modulate by time of day to simulate peak daytime shift pressure.

### Telemetry Datasets (`/Data`)
1. **`syncos_task_execution_log.csv`** (Task Lifecycle):
   - Tracked fields: `Task_ID`, `Task_Type` (Pallet/Material), `Robot_ID`, `Time_Created`, `Time_Assigned`, `Time_Robot_Arrived_Pick`, `Time_Pick_Complete`, `Time_Drop_Complete`.
2. **`syncos_fleet_state_log.csv`** (Fleet State Ticks):
   - Tracked fields: `Log_ID`, `Timestamp`, `Robot_ID`, `Current_State` (`Idle`, `Moving_Loaded`, `Moving_Empty`, `Blocked_Traffic`, `Charging`), `Location_Zone`, `Battery_Level_Pct`.

---

## 🔬 Root Cause Hypotheses & Telemetry Validation

| Hypothesis | Description & Premise | Evaluated Metric | Calculation / Value | Status |
| :--- | :--- | :--- | :--- | :---: |
| **H1: Naive Routing** | Strict FIFO dispatch forces long empty travel distances. | Empty Travel Share | Average empty travel / total cycle time = **25.7%** (119.4s / 465.0s) | **VALIDATED** |
| **H2: Station Handovers** | Shift change handovers bottleneck physical stations. | Station Wait Consistency | Average pickup wait time grouped across 24h = **45.2s avg** (stable 43.3s–47.5s) | **INVALIDATED** |
| **H3: Staging Deadlocks** | Mixed fleet converges on staging zones, causing deadlocks. | Spatial Concentration of Blockages | % of `Blocked_Traffic` states in `Dispatch_Zone` (**34.7%**) & `Aisle_1` (**26.6%**) | **VALIDATED** |
| **H4: Reactive Charging** | "Run-to-depletion" charging pulls robots during peak hours. | Average Charging Threshold | Average battery % when entering `Charging` state = **24.0%** | **VALIDATED** |
| **H5: Task Asymmetry** | Payload imbalance overwhelms one hardware class. | Task Volume Distribution | Task volume split: **54.6% Pallet** vs **45.4% Material** | **INVALIDATED** |
| **H6: Micro-Delays** | Human/environmental pauses cause widespread micro-delays. | Spatial Uniformity of Delays | Delays are non-uniform, concentrated **>61%** in just two zones | **INVALIDATED** |

---

## 🎯 RICE Feature Prioritization & Engineering Roadmap

Using the RICE framework (`Score = (Reach × Impact × Confidence) / Effort`), engineering solutions were prioritized based on validated data findings:

1. **Predictive & Opportunistic Charging Logic (Fixes H4) — Priority 1 (Highest)**
   - **Reach**: 100% fleet | **Impact**: High | **Confidence**: 95% | **Effort**: Low (Parameter/Configuration Update)
   - **Action**: Deprecate the 24% reactive threshold. Force opportunistic charging during scheduled/detected `Idle` windows to keep robots fully charged during peak WMS queuing hours.
2. **Proximity-Weighted Routing (Fixes H1) — Priority 2 (Medium)**
   - **Reach**: 100% tasks | **Impact**: Massive | **Confidence**: 90% | **Effort**: High (Core Orchestration Algorithm Refactor)
   - **Action**: Replace strict FIFO dispatch with real-time spatial proximity scoring (X/Y coordinates relative to pickup points) to eliminate the 25.7% empty travel waste.
3. **Zone-Based Traffic Corridors (Fixes H3) — Priority 3 (Lowest)**
   - **Reach**: ~61% tasks | **Impact**: High | **Confidence**: 85% | **Effort**: Very High (Complex Spatial Logic & Facility Layout Sync)
   - **Action**: Introduce digital one-way routing corridors through `Dispatch_Zone` and `Aisle_1` to resolve high-density traffic congestion.

---

## 📈 Throughput Metrics & Improvement Projections

- **Current Baseline**:
  - **Total Tasks Completed**: 5,000 tasks
  - **Total Active Fleet Hours**: 132.8 hours
  - **Baseline Throughput**: **37.64 tasks / hour** (Average Cycle Time: 465.0 seconds)

### Projected Improvements
- **Solution 1 (Predictive Charging)**:
  - Reclaims ~66.88 peak active hours by shifting charging into idle windows.
  - Yields **+518 additional tasks** → **41.54 tasks / hour** (**+10.4% throughput increase**).
- **Solution 2 (Proximity Routing)**:
  - Assumes a conservative 50% reduction in empty travel time (saving 59.7s per task, reducing cycle time to 405.3s).
  - Yields **5,736 total tasks** from the same active fleet hours → **43.18 tasks / hour** (**+14.7% throughput increase**).

---

## 📂 Repository Structure & File Index

```text
├── README.md                           # Overview, telemetry analysis & roadmap index
├── SyncOS Final Analysis.pdf           # Comprehensive case study, hypotheses & telemetry findings
├── SyncOS Orchestration Assumptions.pdf # Fleet baseline context & technical assumptions
├── SyncOS RICE Prioritization.pdf      # Feature prioritization matrix & evaluation criteria
├── SyncOS Throughput Projections.pdf   # Quantitative mathematical modeling & impact analysis
└── Data/
    ├── Data Generation Philosophy.pdf  # Synthetic data generation methodology & strategy
    ├── SyncOS Telemetry Data Schema.pdf# Data schema documentation for logs
    ├── data_generator.py               # Python script for generating procedural telemetry logs
    ├── syncos_fleet_state_log.csv      # Telemetry dataset: Fleet state, battery & zone locations
    └── syncos_task_execution_log.csv   # Telemetry dataset: Task creation, pick & drop execution timestamps
```
