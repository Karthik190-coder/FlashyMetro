# FLASHYMETRO

A shortest-path routing engine and live route visualizer for the Kochi Metro **Blue Line** (Aluva ↔ Tripunithura), built to actually understand — not just use — Dijkstra's algorithm and a small full-stack system around it.

## What it does

- Models the real Kochi Metro Blue Line (25 stations, official KMRL order) as a weighted graph, where stations are nodes and travel time between adjacent stations is the edge weight.
- Extends the graph with the real, publicly announced **Phase 2 (Pink Line) branch** — Palarivattom Junction through InfoPark 2 — connected at its real junction point (Palarivattom), even though Phase 2 isn't operational yet. This gives the network an actual hub-and-spoke structure instead of a single line with no alternatives.
- Computes the shortest (fastest) route between any two stations using a heap-optimized Dijkstra's algorithm.
- Serves routes over a small Flask API.
- Renders the route on an interactive Leaflet map — pins for each stop, a line connecting them, and the total travel time — with dropdown selectors (populated live from `/stops`) so users don't need to know exact station names in advance.
- Supports simulated **disruptions**: temporarily closing a connection between two adjacent stations (e.g. a signal fault or flooding) and watching the algorithm either reroute or correctly report that no path exists, then reopening it to restore normal service. Because the main line and the Kakkanad branch only share the single Palarivattom junction, disruptions demonstrate real partial fault-tolerance: a fault on one branch doesn't affect the other, but a fault at the shared junction affects both.
- Input is case-insensitive and validated (missing stops, unknown stop names, disconnected routes) rather than crashing on bad input.

## Why Dijkstra, and why the heap version

A city transit network is naturally a graph: stations as nodes, direct connections as edges, travel time as weight. Finding the fastest route between two stations is a shortest-path problem, which is exactly what Dijkstra's algorithm solves for graphs with non-negative weights.

The naive version of Dijkstra repeatedly scans every unvisited node to find the closest one — O(V²) time. This project uses a **min-heap** (Python's `heapq`) to always pop the closest known station in O(log V) instead, bringing the overall complexity down to O((V + E) log V). With the Phase 2 branch included, the graph now has 35 stations and a real junction, so the algorithm has to genuinely choose between reachable stations by weight rather than just walking a line — closer to what this optimization is actually built for.

## Architecture

```
MetroPulse.py   -- the graph (graph1), coordinates (stop_coords), and the
                   Dijkstra implementation (dijkstra_opti), plus
                   close_connection / reopen_connection for disruption simulation
app.py          -- Flask API: /route, /stops, /disrupt, /reopen
index.html      -- Leaflet-based frontend: search inputs, disruption controls,
                   map rendering
```

### API

| Route | Params | Description |
|---|---|---|
| `GET /route` | `start`, `end` | Returns the fastest path and total time between two stations |
| `GET /stops` | — | Returns coordinates for every station |
| `GET /disrupt` | `stop_a`, `stop_b` | Temporarily removes the direct connection between two adjacent stations |
| `GET /reopen` | `stop_a`, `stop_b` | Restores a previously closed connection |

All stop name matching is case-insensitive (`aluva`, `Aluva`, and `ALUVA` all resolve correctly).

## Known limitations / honesty section

- The Blue Line portion of the graph is real and operational; the **Phase 2 (Pink Line) branch is not yet operational** as of this writing — it's included specifically to give the routing engine a real junction and a fault-tolerance case to demonstrate, using KMRL's own announced station list and junction point, not an invented shortcut.
- Station coordinates are **interpolated in segments between approximate real anchor points** (not a single straight line across the whole network), which follows the real corridor's curve reasonably well but is not survey-grade GPS data.
- Edge weights (travel time between adjacent stations) are a rough approximation based on published average travel pace and segment lengths, not the exact KMRL timetable.
- Because the Blue Line itself has no branches, a normal route query on it only ever has one possible path — the interesting Dijkstra behavior (rerouting vs. correctly failing) shows up either in the disruption feature, or in routes that cross into the Phase 2 branch.

## Future work

- Replace segment-interpolated coordinates with verified survey-grade station coordinates.
- Real-time simulation of multiple trains moving along the line concurrently (would need WebSockets/Flask-SocketIO and background threads).
- An AI-driven "crisis dispatcher" that, on a disruption, estimates passenger/time impact and suggests operational responses — the current `/disrupt` endpoint is the algorithmic foundation this would sit on top of.
- A compiled C implementation of the pathfinder loaded via `ctypes`/Cython, for a low-level performance comparison against the pure-Python heap version.

## Running it

```bash
pip install flask flask-cors
python app.py
```

Then open `index.html` in a browser (Flask serves the API on `http://127.0.0.1:5000`).