# Messaging Service App — Flask, Socket.IO, JavaScript

*CMPSC 297 — Special Topics · The Pennsylvania State University · 2023*

**[Live Showcase →](https://halkhoori2000.github.io/Messaging-Service-App/)**

A real-time multi-channel chat application where users log in, create channels, send messages, and delete their own messages — all without page reloads. Built with Flask-SocketIO on the backend and a hand-rolled JavaScript component system on the frontend.

The entire UI is built in vanilla JavaScript using a custom `el()` helper that mirrors `React.createElement` — elements are created programmatically, state is managed with a `setState` + re-render pattern, and the DOM is rebuilt on every state change. Socket.IO handles bidirectional communication between clients and the server. Messages are stored in-memory (Python dicts) and capped at 100 per channel; channels and users persist for the lifetime of the server process.

---

## Use Cases
- **Multi-channel chat**: users create named channels and switch between them in a sidebar; each channel maintains its own message history
- **Real-time messaging**: messages broadcast instantly to all users in the same channel via Socket.IO room events — no polling
- **Username persistence**: the username is saved to `localStorage` so users rejoin their previous channel on page reload without re-entering credentials
- **Message deletion**: users can delete any of their own messages; the deletion broadcasts to all channel members and removes it from their view immediately
- **Session management**: users can leave a channel (stay logged in) or fully log out; logging out clears localStorage and resets state

## Challenges
- **No framework — custom component system**: the entire UI is built with a hand-rolled `el(tagName, props, ...children)` function and a `setState` → `render()` cycle — functionally equivalent to React's component model but implemented in ~30 lines
- **In-memory storage**: channels and messages live in Python dicts for the server's lifetime — a server restart clears all history; a persistent store (Redis, PostgreSQL) would be needed for production
- **Socket.IO room management**: each channel maps to a Socket.IO room; `join_room` / `leave_room` are called on every channel switch to ensure broadcasts only reach the right users
- **Message deletion sync**: deletions are matched by username + message text + ISO timestamp triplet — no message IDs in the data model; a UUID per message would be more robust

---

## Tech Stack

| Item | Detail |
|---|---|
| Backend | Python · Flask · Flask-SocketIO |
| Transport | WebSockets via Socket.IO |
| Frontend | Vanilla JavaScript · custom `el()` component system |
| UI | Bootstrap 5 (CDN) |
| Storage | In-memory Python dicts (no database) |
| Auth | Username-based · localStorage persistence |

---

## Project Structure

```
Messaging-Service-App/
├── application.py          ← Flask app + all Socket.IO event handlers
├── requirements.txt        ← Flask, Flask-SocketIO
└── templates/
    └── index.html          ← Single-page app: Socket.IO client + full JS UI
```

---

## Run

**Requirements:** Python 3.8+

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set secret key
export SECRET_KEY='your-secret-key-here'

# 3. Start the server
python3 application.py
# Open http://localhost:5000
```

---

## Course

CMPSC 297 — Special Topics  
The Pennsylvania State University · 2023
