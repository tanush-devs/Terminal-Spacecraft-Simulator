# ORBITAL-7 — Unit Test Plan

Covers everything not already handled by `test_chunkmanager.py` and `test_camera_renderer.py`.
Each item = one test function. Grouped by file, then by function under test.

---

## `test_rocket.py`

### `update_thrust`
- [ ] `thrust_increase=True` raises thrust by `Thrust_Buildup_Rate * dt`
- [ ] `thrust_decrease=True` lowers thrust by `Counter_Thrust_Buildup_Rate * dt`
- [ ] thrust clamps at `max_thrust` (5) and won't exceed it even with large dt
- [ ] thrust clamps at `max_counter_thrust` (-3) and won't go below it
- [ ] **neither key pressed → thrust stays exactly the same** (confirms no auto-decay; this is intentional throttle behavior, worth locking in with a test so it isn't "fixed" accidentally later)
- [ ] both `thrust_increase` and `thrust_decrease` True simultaneously → net change is `(increase_rate - decrease_rate) * dt`

### `update_angle`
- [ ] `rotate_right=True` → `angular_acceleration` becomes `0.3`
- [ ] `rotate_left=True` → `angular_acceleration` becomes `-0.3`
- [ ] neither pressed → `angular_acceleration` resets to `0.0`
- [ ] `angular_velocity` clamps at `max_angular_velocity` (1) with sustained rotation
- [ ] `angular_velocity` clamps at `-max_angular_velocity` (-1)
- [ ] `angle` wraps correctly past `2π` (e.g. start near `2π - 0.05`, rotate forward, result should be small positive, not `> 2π`)
- [ ] `angle` wraps correctly for negative overflow (rotate left from `angle=0`)

### `update_rocket_emoji`
One test per direction, feeding `self.angle` directly and calling `update_rocket_emoji()`:
- [ ] `angle = 0` → `ROCKET_FACING_NORTH`
- [ ] `angle` just below `2π` (e.g. `2π - 0.01`) → `ROCKET_FACING_NORTH` (**this is the exact case the earlier chained-comparison bug broke** — keep this test permanently as a regression guard)
- [ ] `angle = π/4` → `ROCKET_FACING_NORTH_EAST`
- [ ] `angle = π/2` → `ROCKET_FACING_EAST`
- [ ] `angle = 3π/4` → `ROCKET_FACING_SOUTH_EAST`
- [ ] `angle = π` → `ROCKET_FACING_SOUTH`
- [ ] `angle = 5π/4` → `ROCKET_FACING_SOUTH_WEST`
- [ ] `angle = 3π/2` → `ROCKET_FACING_WEST`
- [ ] `angle = 7π/4` → `ROCKET_FACING_NORTH_WEST`
- [ ] exact boundary value (e.g. `angle = π/8` precisely) — document/confirm current behavior (falls through to next bin since bounds are strict `<`), so it's a documented gap, not a surprise

### `update_accelaration`
- [ ] `angle=0`, `thrust=5` → `ax ≈ 0`, `ay ≈ -5` (thrust pushes "up"/north)
- [ ] `angle=π/2`, `thrust=5` → `ax ≈ 5`, `ay ≈ 0`
- [ ] `thrust=0` → `ax=0`, `ay=0` regardless of angle

### `update_position`
- [ ] constant `ax`/`ay` over one `dt` step updates `vx`/`vy` by `a*dt`, then `x`/`y` by `v*dt` (semi-implicit Euler order — position uses the *already-updated* velocity)
- [ ] `dt=0` → no change to position or velocity

### `current_speed` / `current_acceleration`
- [ ] `vx=3, vy=4` → `current_speed() == 5.0`
- [ ] `ax=0, ay=0` → `current_acceleration() == 0.0`

### `update_physics` (integration)
- [ ] confirms call order matters: rotating and thrusting in the same `update_physics` call produces acceleration based on the **new** angle, not the previous frame's angle

---

## `test_telementary.py`

### `get_telementary_data`
- [ ] returns all five expected top-level sections, **in order**: `POSITION`, `VELOCITY`, `ACCELERATION`, `ORIENTATION`, `GENERAL`
- [ ] `POSITION["Y"]` and `VELOCITY["Y"]`/`["Y"]` etc. are **sign-flipped** from the raw rocket values (`-rocket.y`, `-rocket.vy`, `-rocket.ay`) — easy to break accidentally, worth a dedicated test
- [ ] all numeric values rounded to 3 decimals (feed a long-decimal float, confirm truncation)
- [ ] `GENERAL["Chunk"]` matches `(chunk_x, -chunk_y)` from `world_to_chunk_coords`, not `(chunk_y, chunk_x)` — order/sign are both easy to get backwards
- [ ] `ORIENTATION["Angle"]` is in **degrees**, not radians

### `get_display_list`
- [ ] first two lines are always the header (`"\t◈ TELEMETRY"`) and a separator of length `width - 2`
- [ ] each section produces: 1 header line + 1 line per field + 1 blank line
- [ ] adding a fake extra section to the data dict produces corresponding extra lines with **zero changes to this function** (this is the exact sanity check described in `ORBITAL_7_Telemetry_Step_1.md` §14 — worth automating instead of doing it by hand)
- [ ] field line format matches `f"    {field}: {value}"` exactly (leading 4 spaces)

### `scroll`
- [ ] scrolling down (positive `dy`) decreases `scroll_offset` — confirm this is the intended direction, since `scroll_offset -= dy`
- [ ] `scroll_offset` clamps at `0` (can't go negative)
- [ ] `scroll_offset` clamps at `max_offset` (can't exceed it)
- [ ] repeated small scrolls accumulate correctly before hitting a clamp

---

## `test_input_handler.py`

Construct `InputHandler` with a mock/stub `renderer` (needs `renderer.telementary.scroll` to exist as a callable — a `Mock()` is fine, don't need a real `Telementary`). Call `on_press`/`on_release` directly with fake key objects instead of driving real hardware.

- [ ] pressing `'w'` or `'W'` sets `thrust_increase = True`; releasing sets it back to `False`
- [ ] same pair of tests for `'s'/'S'` → `thrust_decrease`
- [ ] same pair for `'a'/'A'` → `rotate_left`
- [ ] same pair for `'d'/'D'` → `rotate_right`
- [ ] `keyboard.Key.esc` on press sets `game_is_running = False`
- [ ] `keyboard.Key.esc` on release **also** sets `game_is_running = False` (confirms the fix — it used to call `os._exit(0)` and skip curses cleanup)
- [ ] an unrelated key (e.g. `keyboard.KeyCode.from_char('q')`) leaves all flags untouched and doesn't raise
- [ ] a special key with no `.char` attribute (e.g. `keyboard.Key.space`) doesn't raise (`getattr(key, 'char', None)` should return `None` safely)
- [ ] constructor wires `mouse.Listener(on_scroll=...)` to the exact `renderer.telementary.scroll` method passed in (patch `pynput.mouse.Listener` and assert the `on_scroll` kwarg it was called with)

---

## `test_camera_renderer.py` — additions to your existing file

Your current tests only check positive coordinates and one hand-picked offset. Add:

- [ ] `get_pad_top_chunk` + `get_view_bounds` chained together (call the first, then feed its result straight into the second) rather than manually setting `pad_top_chunk`/`pad_left_chunk` — this is closer to how `render_world` actually uses them
- [ ] negative rocket coordinates (e.g. `x=-5, y=-5`)
- [ ] rocket position exactly on a chunk boundary (e.g. `x=32, y=32`)
- [ ] fractional rocket position (e.g. `x=16.5, y=16.5`) — confirms rounding behavior explicitly, since Python's `round()` uses round-half-to-even and this can surprise you at `.5`
- [ ] `screen_player_y`/`screen_player_x` returned by `get_view_bounds` is **always** `screen_h // 2`, `(screen_w // 2 // 2) * 2` regardless of rocket position (this should be a mathematical identity — worth asserting directly rather than only implicitly through the existing tests)

### `test_renderer_resize.py` (new file, or fold into the above)
Mock out `curses` calls (`curses.newpad`, `curses.newwin`, etc.) or patch them, since these need a real terminal otherwise.

- [ ] `resize_renderer(appstate)` sets `self.reprint_pad = True` (**regression test** — this used to be missing, causing the pad to never repaint after a terminal resize)
- [ ] `process_resize(appstate)` calls `resize_renderer(appstate)` only when `stdscr.getmaxyx()` differs from stored `screen_h`/`screen_w`
- [ ] `process_resize(appstate)` does **not** call `resize_renderer` when dimensions are unchanged
- [ ] `process_resize(appstate)` doesn't raise `TypeError` for a missing argument (**regression test** — this used to crash with `resize_renderer()` missing `appstate`)
- [ ] pad/viewport dimension math: given a screen size, `pad_height`/`pad_width` come out to `((screen_h // CHUNK_SIZE) + 3) * CHUNK_SIZE` and `((screen_w // (CHUNK_SIZE*2)) + 3) * CHUNK_SIZE * 2`

### `render_world` chunk-reprint logic (extract-and-test, or integration test with mocked pad/chunk manager)
- [ ] first call ever (`lastRenderCy`/`lastRenderCx` both `None`) → `reprint_pad` is forced `True`
- [ ] same chunk as last frame → `reprint_pad` is `False`, tile-drawing loop (`viewport.addstr`) is **not** called again
- [ ] moved into a new chunk since last frame → `reprint_pad` is `True`, `chunk_mgr.unload_inactive_chunks` is called
- [ ] `world_to_chunk_coords` is called with `(rocket.y, rocket.x)` in that order, not `(x, y)` (**regression test** — this was previously swapped and threw off reprint/unload timing whenever `x != y`)

---

## `test_appstate.py`

- [ ] `AppState()` defaults: `is_running=True`, `target_fps=30`
- [ ] `appstate.rocket` is a `Rocket` instance
- [ ] `appstate.chunk_manager` is a `ChunkManager` instance with `seed=2009`

---

## Notes on things that are hard/awkward to unit test as-is

- **`main.py`** — module-level script wrapped in `curses.wrapper(main)`, runs on import. Not realistically unit-testable without refactoring the game loop body into a testable function (e.g. `def run_frame(appstate, renderer, inputhandler, dt): ...`). Worth doing if you want CI coverage on the main loop itself.
- **`rendering.py` fully-drawn frames** — anything that actually calls `stdscr.addstr`/`noutrefresh`/`doupdate` needs a real or mocked curses window. Either patch `curses` module functions with `unittest.mock.patch`, or pull the pure math (offsets, dimensions, reprint-trigger conditions) into small standalone functions you can test without curses at all — this is generally the better long-term move, since it also makes the "shaking" investigation from earlier much easier to test going forward.
- **`input_handler.py` real listener threads** — `poll_action()` itself (which starts `pynput` listeners) is an integration concern, not a unit-test concern. Test `on_press`/`on_release` directly as plain methods instead.