# Intelligent Agent for Sokoban / Pressure-Plate Puzzle

<p align="center">
  <img src="https://img.shields.io/badge/Language-Python-blue" />
  <img src="https://img.shields.io/badge/AI-Search%20Algorithms-purple" />
  <img src="https://img.shields.io/badge/Algorithm-A*-orange" />
  <img src="https://img.shields.io/badge/Heuristics-Custom-success" />
</p>

An intelligent agent developed to solve a Sokoban-style pressure-plate puzzle.

The project demonstrates practical application of **state-space search**, **heuristic design**, and classical **AI planning algorithms**.

---

## Problem Description

The environment is a grid-based puzzle where the agent must navigate through rooms containing:
- Doors and corresponding keys
- Pressure plates that affect the environment
- Obstacles and constrained movement

The objective is to find a valid sequence of actions that leads the agent to the goal state.

---

## Algorithms Implemented

- ⭐ A* Search
- 🔍 Greedy Best-First Search (GBFS)

Both algorithms operate over an explicit state-space representation of the environment.

---

##  Heuristic Design

A custom heuristic function was implemented, combining:

- 📏 Manhattan distance for spatial guidance
- 🚪 Door penalties to account for blocked paths and required keys

This heuristic improves search efficiency while maintaining admissibility where required.


---

## Project Structure

```bash
.
├── ex1.py        # Main agent logic
├── search.py    # Search algorithms (A*, GBFS)
├── utils.py     # Utility functions and helpers
└── README.md
