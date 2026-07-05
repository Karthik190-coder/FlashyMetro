# MetroPulse

A shortest-path routing engine and live route visualizer for the Kochi Metro **Blue Line** (Aluva ↔ Tripunithura), built to actually understand — not just use — Dijkstra's algorithm and a small full-stack system around it.

## What it does

- Models the real Kochi Metro Blue Line (25 stations, official KMRL order) as a weighted graph, where stations are nodes and travel time between adjacent stations is the edge weight.
- Computes the shortest (fastest) route between any two stations using a heap-optimized Dijkstra's algorithm.
- Serves routes over a small Flask API.
- Renders the route on an interactive Leaflet map — pins for each stop, a line connecting them, and the total travel time.
- Supports simulated **disruptions**: temporarily closing a connection between two adjacent stations (e.g. a signal fault or flooding) and watching the algorithm either reroute or correctly report that no path exists, then reopening it to restore normal service.
- Input is case-insensitive and validated (missing stops, unknown stop names, disconnected routes) rather than crashing on bad input.

## Why Dijkstra, and why the heap version

A city transit network is naturally a graph: stations as nodes, direct connections as edges, travel time as weight. Finding the fastest route between two stations is a shortest-path problem, which is exactly what Dijkstra's algorithm solves for graphs with non-negative weights.

The naive version of Dijkstra repeatedly scans every unvisited node to find the closest one — O(V²) time. This project uses a **min-heap** (Python's `heapq`) to always pop the closest known station in O(log V) instead, bringing the overall complexity down to O((V + E) log V). On a real transit network with many stations and connections, that difference matters a lot more than it does on a handful of test stops — even though the current Blue Line model is a single line and doesn't yet have branching routes to fully showcase it.

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

- The current graph reflects the **real, operational Blue Line only** — a single line with no branches or interchanges. Kochi Metro's Phase 2 (Pink Line) is still under construction and not yet operational, so it isn't included here. This means a normal route query only ever has one possible path; the disruption feature is the main place where the algorithm's behavior (rerouting vs. correctly failing) is actually visible.
- Station coordinates are **interpolated in a straight line** between Aluva and Tripunithura's real coordinates, not traced from the real curved alignment of the line. Good enough for pins to land in the right order and rough area; not survey-accurate.
- Edge weights (travel time between adjacent stations) are a rough approximation based on published average end-to-end travel time, not the exact KMRL timetable.

## Future work

- Add Phase 2 (Pink Line) once it's operational, introducing real interchanges and giving Dijkstra actual route choices to weigh.
- Real-time simulation of multiple trains moving along the line concurrently (would need WebSockets/Flask-SocketIO and background threads).
- An AI-driven "crisis dispatcher" that, on a disruption, estimates passenger/time impact and suggests operational responses — the current `/disrupt` endpoint is the algorithmic foundation this would sit on top of.
- A compiled C implementation of the pathfinder loaded via `ctypes`/Cython, for a low-level performance comparison against the pure-Python heap version.

## Running it

```bash
pip install flask flask-cors
python app.py
```

Then open `index.html` in a browser (Flask serves the API on `http://127.0.0.1:5000`).