# ORBITAL-7 — Telemetry Upgrade
## Step 1: Data-Driven Telemetry

> **Goal:** Replace hardcoded telemetry rendering with a small, structured data layer.
>
> **Not part of Step 1:** scrolling, mouse input, viewport management, or telemetry UI redesign.

---

# 1. What We're Fixing

The current telemetry renderer has a problem that will get worse as ORBITAL-7 grows.

It may currently look conceptually like:

```python
window.addstr(...)
window.addstr(...)
window.addstr(...)
window.addstr(...)
# ... many more lines
```

Every new telemetry value requires another rendering statement.

That creates two mixed responsibilities:

- **What data should telemetry contain?**
- **How should that data be displayed?**

Step 1 separates them.

The target architecture is:

```text
Rocket / AppState
       │
       │ raw values
       ▼
build_telemetry()
       │
       │ structured telemetry data
       ▼
telemetry_to_lines()
       │
       │ display-ready lines
       ▼
renderer
       │
       ▼
curses window
```

The renderer should eventually care very little about *which* telemetry fields exist.

---

# 2. The Core Design Principle

## Data first, rendering second

Instead of writing:

```python
window.addstr(1, 0, f"X : {rocket.x}")
window.addstr(2, 0, f"Y : {rocket.y}")
window.addstr(3, 0, f"X : {rocket.vx}")
```

we want:

```python
telemetry_data = build_telemetry(rocket, chunk)
```

which produces something like:

```python
{
    "POSITION": {
        "X": 0.0,
        "Y": -0.0,
    },

    "VELOCITY": {
        "X": 0.0,
        "Y": -0.0,
        "MAGNITUDE": 0.0,
    },

    "ACCELERATION": {
        "X": 0.0,
        "Y": -0.0,
        "MAGNITUDE": 0.0,
    },

    "GENERAL": {
        "THRUST": 0,
        "CHUNK": (0, 0),
    },
}
```

The dictionary describes the **content and order** of telemetry.

The renderer later decides how that content is drawn.

---

# 3. Why Use Sections?

Telemetry naturally has groups of related values.

For example:

```text
POSITION
    X
    Y

VELOCITY
    X
    Y
    MAGNITUDE

ACCELERATION
    X
    Y
    MAGNITUDE
```

Representing those groups directly in the data makes the structure easy to understand.

```python
"POSITION": {
    "X": ...,
    "Y": ...,
}
```

This also makes future additions straightforward:

```python
"ROTATION": {
    "ANGLE": ...,
    "ANGULAR_VELOCITY": ...,
}
```

or:

```python
"ORBIT": {
    "ALTITUDE": ...,
    "APOAPSIS": ...,
    "PERIAPSIS": ...,
}
```

No new rendering architecture is needed.

---

# 4. Where Does `telemetry_data` Come From?

Create a small telemetry module, for example:

```text
telemetry.py
```

Its first responsibility is to construct the current telemetry snapshot.

Conceptually:

```python
def build_telemetry(rocket, chunk):
    return {
        ...
    }
```

The function receives the objects that already contain the simulation state.

It does **not** own the spacecraft physics.

It does **not** update the rocket.

It does **not** render anything.

It simply answers:

> "Given the current simulation state, what information should telemetry display?"

---

# 5. Keep Physics Out of Telemetry

Telemetry can calculate simple *derived values* that are useful for display.

For example:

```python
speed = (rocket.vx ** 2 + rocket.vy ** 2) ** 0.5
```

Then:

```python
"VELOCITY": {
    "X": rocket.vx,
    "Y": rocket.vy,
    "MAGNITUDE": speed,
}
```

That's reasonable because telemetry is preparing information for display.

But don't start putting simulation rules here.

Avoid things like:

```python
rocket.update_physics(...)
```

or:

```python
rocket.apply_gravity(...)
```

Telemetry should **observe** the simulation, not control it.

A useful mental model:

```text
Physics → produces state
Telemetry → reads state
Renderer → displays telemetry
```

---

# 6. Step 1 Implementation

## Step 1A — Create the telemetry data builder

Create:

```text
telemetry.py
```

Start with the fields that already exist in ORBITAL-7.

Conceptually:

```python
def build_telemetry(rocket, chunk):
    speed = (rocket.vx ** 2 + rocket.vy ** 2) ** 0.5
    acceleration = (rocket.ax ** 2 + rocket.ay ** 2) ** 0.5

    return {
        "POSITION": {
            "X": rocket.x,
            "Y": rocket.y,
        },

        "VELOCITY": {
            "X": rocket.vx,
            "Y": rocket.vy,
            "MAGNITUDE": speed,
        },

        "ACCELERATION": {
            "X": rocket.ax,
            "Y": rocket.ay,
            "MAGNITUDE": acceleration,
        },

        "GENERAL": {
            "THRUST": rocket.thrust,
            "CHUNK": chunk,
        },
    }
```

### Important

Do **not** blindly copy attribute names.

Use the actual names from the current ORBITAL-7 `Rocket` / `AppState`.

For example, if your acceleration is stored differently, use that existing representation.

The goal is the architecture, not forcing a new naming convention onto the project.

---

# 7. Step 1B — Convert Data Into Display Lines

The renderer should ideally not have to understand the nested dictionary.

Give it a simple list of lines.

Create:

```python
def telemetry_to_lines(telemetry_data):
    lines = []

    for section, values in telemetry_data.items():
        lines.append(section)

        for label, value in values.items():
            lines.append(f"  {label} : {value}")

        lines.append("")

    return lines
```

For this data:

```python
{
    "POSITION": {
        "X": 0.0,
        "Y": -0.0,
    },

    "VELOCITY": {
        "X": 0.0,
        "Y": -0.0,
        "MAGNITUDE": 0.0,
    },
}
```

you get approximately:

```python
[
    "POSITION",
    "  X : 0.0",
    "  Y : -0.0",
    "",
    "VELOCITY",
    "  X : 0.0",
    "  Y : -0.0",
    "  MAGNITUDE : 0.0",
    "",
]
```

Now the renderer has a very simple job:

> "Here are the lines. Draw them."

---

# 8. Why `dict` Ordering Is Enough

Python dictionaries preserve insertion order.

Therefore:

```python
{
    "POSITION": ...,
    "VELOCITY": ...,
    "ACCELERATION": ...,
    "GENERAL": ...,
}
```

will be iterated in that order.

Likewise:

```python
"VELOCITY": {
    "X": ...,
    "Y": ...,
    "MAGNITUDE": ...,
}
```

keeps that field ordering.

There is no need for:

- `OrderedDict`
- an enum system
- a telemetry registration framework
- a custom section class
- a configuration language

Not yet, anyway.

**Keep it boring.**

The project is still young, and this structure is already flexible enough.

---

# 9. Step 1C — Replace Hardcoded Rendering

Before:

```python
window.addstr(...)
window.addstr(...)
window.addstr(...)
window.addstr(...)
window.addstr(...)
```

After:

```python
telemetry_data = build_telemetry(rocket, chunk)
lines = telemetry_to_lines(telemetry_data)

for row, line in enumerate(lines):
    window.addstr(row, 0, line)
```

That's the important transition.

The renderer no longer needs:

```python
if telemetry_position:
    ...
if telemetry_velocity:
    ...
if telemetry_acceleration:
    ...
```

It simply iterates.

---

# 10. The Renderer Should Become "Dumb"

This is intentional.

A good telemetry renderer should not need to know:

- what velocity means
- how speed is calculated
- where the rocket's position comes from
- what fields will exist next month
- whether an `ORBIT` section exists
- whether a `FUEL` section exists

It should mostly know:

```text
I have some lines.
I have a window.
Draw the lines.
```

That means adding:

```python
"FUEL": {
    "CURRENT": rocket.fuel,
    "MAX": rocket.max_fuel,
}
```

should require **zero changes to the rendering loop**.

That's the real test of whether Step 1 worked.

---

# 11. Formatting: Keep It Simple for Now

For the first implementation, this is perfectly acceptable:

```python
f"  {label} : {value}"
```

Later, you can improve formatting.

For example:

```text
X :       12.45
Y :       -8.21
MAGNITUDE : 14.91
```

or use different precision for different values.

But **don't build a formatting framework during Step 1**.

The objective right now is:

```text
hardcoded telemetry
        ↓
structured telemetry
        ↓
iterated rendering
```

Formatting polish can come later.

---

# 12. What Should NOT Be Added in Step 1

Do not combine this step with:

### ❌ Mouse handling

No:

```python
curses.mousemask(...)
```

yet.

### ❌ Scrolling

No:

```python
scroll_offset
```

yet.

### ❌ Viewport calculations

No:

```python
visible_height
max_scroll
```

yet.

### ❌ Telemetry window resizing logic

Leave the existing window/layout system alone.

### ❌ Major InputHandler changes

Don't touch the input architecture unless the current telemetry renderer requires a tiny integration change.

### ❌ New physics

Telemetry should use the values ORBITAL-7 already has.

---

# 13. Testing Step 1

Before moving to scrolling, make sure the refactor behaves exactly like the old telemetry.

## Visual test

Compare the old and new panel.

Check:

- [ ] Position still appears
- [ ] Velocity still appears
- [ ] Acceleration still appears
- [ ] Thrust still appears
- [ ] Chunk still appears
- [ ] Section ordering is correct
- [ ] Field ordering is correct
- [ ] Spacing is acceptable
- [ ] No unexpected extra lines appear
- [ ] No existing simulation behavior changed

The important principle:

> **A refactor should change the architecture, not accidentally change the behavior.**

---

# 14. A Very Useful Test

After everything works, temporarily add a fake section:

```python
"TEST": {
    "VALUE": 123,
}
```

You should **not** need to touch the renderer.

If the panel automatically displays:

```text
TEST
  VALUE : 123
```

then the data-driven architecture is working.

Remove the test section afterward.

This is a simple but powerful sanity check.

---

# 15. Future Expansion

Once Step 1 is complete, adding telemetry becomes easy.

For example:

```python
"ROTATION": {
    "ANGLE": rocket.angle,
    "ANGULAR_VELOCITY": rocket.angular_velocity,
}
```

Then later:

```python
"FUEL": {
    "CURRENT": rocket.fuel,
    "MAX": rocket.max_fuel,
}
```

Then eventually:

```python
"ORBIT": {
    "ALTITUDE": ...,
    "APOAPSIS": ...,
    "PERIAPSIS": ...,
    "ECCENTRICITY": ...,
}
```

The renderer doesn't need to change.

That's exactly what we want.

---

# 16. Mental Model

If you're coding this at school and don't have much time, remember just this:

```text
ROCKET
  ↓
build_telemetry()
  ↓
DICTIONARY
  ↓
telemetry_to_lines()
  ↓
LIST OF STRINGS
  ↓
RENDERER
  ↓
CURSES WINDOW
```

### Responsibilities

| Component | Responsibility |
|---|---|
| `Rocket` / `AppState` | Own simulation state |
| `build_telemetry()` | Collect/organize telemetry |
| `telemetry_to_lines()` | Turn data into display lines |
| Renderer | Draw lines |
| InputHandler | **Not touched in Step 1** |

---

# 17. Definition of Done

Step 1 is complete when all of these are true:

- [ ] Telemetry values are no longer individually hardcoded in the renderer
- [ ] Telemetry is represented by a structured dictionary
- [ ] Sections have a predictable order
- [ ] Fields have a predictable order
- [ ] A function builds telemetry from existing simulation state
- [ ] A function converts telemetry into display lines
- [ ] Renderer iterates over those lines
- [ ] Adding a new telemetry field does not require a new `addstr()` call
- [ ] Existing telemetry still looks correct
- [ ] No scrolling/mouse logic has been added yet
- [ ] No world/pad rendering behavior has been affected

---

# 18. The One Rule to Remember

> **Telemetry decides WHAT to display. Renderer decides HOW to display it.**

If you keep that boundary clean, Step 2 — the scrollable viewport — becomes much easier.

The renderer will already have a simple list of lines.

Then Step 2 only has to answer:

```text
Which portion of these lines is currently visible?
```

And that's where `scroll_offset` and mouse-wheel input can be added.
