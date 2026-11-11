-- DeSmuME 0.9.13 (x64) Lua capture script for the DQM J2 Pro decompilation.
--
-- Purpose: dump the ARM9 main-RAM window 0x02000000..0x021D7240 (1,929,792 bytes)
-- after a configurable warm-up, optionally after a scripted button timeline, so the
-- BSS-resident species roster (0x021C4BF8) and the script-VM text block
-- (0x020FB264) can be sliced out by ops/ram_capture.py.
--
-- This file is the authoritative script. DeSmuME cannot take a Lua script on the
-- command line (0.9.13 --help has no such option), so ops/emulate_capture.py writes
-- a one-line shim `<rom>.lua` next to DeSmuME_0.9.13_x64.exe and sets
-- [Scripting] AutoLoad=1 in desmume.ini. On ROM load DeSmuME opens a Lua window,
-- sets the script path (which fires EN_CHANGE -> UpdateFileEntered -> Run) and the
-- script below executes with no user interaction.
--
-- Configuration is read from the environment so the Python wrapper stays the single
-- source of truth and this file needs no rewriting per capture:
--   DQM_CAPTURE_OUT      absolute path of the raw dump to write   (required)
--   DQM_CAPTURE_LOG      absolute path of a plain-text log        (optional)
--   DQM_CAPTURE_FRAMES   frames to advance before dumping         (default 300)
--   DQM_CAPTURE_TIMELINE button timeline applied before the dump  (default empty)
--                        "FRAMES:BUTTONS;FRAMES:BUTTONS;..." e.g.
--                        "120:;20:START;40:;10:A" (empty BUTTONS = inert wait)
--   DQM_CAPTURE_EXIT     "1" (default) -> os.exit(0) after the dump
--   DQM_CAPTURE_SAVESTATE  optional DeSmuME state slot N to write before the dump
--   DQM_CAPTURE_LOADSTATE  optional DeSmuME state slot N to load before the timeline
--   DQM_CAPTURE_PAUSE    "1" -> emu.pause() after the dump instead of exiting, so a
--                        screenshot taken by the wrapper shows exactly this state
--
-- The dump window is fixed by the manifest (main = 0x02000000 + 930560 image +
-- 999232 BSS = 0x021D7240). Do not "improve" it to a 4 MiB window here; a larger
-- dump is accepted by the tool but keeping it exact makes the file easier to verify.

local BASE = 0x02000000
local LENGTH = 1929792 -- 0x021D7240 - 0x02000000 (override with DQM_CAPTURE_LENGTH)

local unpack = unpack or table.unpack

local function now()
  return string.format("%.3f", os.clock())
end

local function open_log()
  local path = os.getenv("DQM_CAPTURE_LOG")
  if not path or path == "" then
    return nil
  end
  local handle = io.open(path, "a")
  return handle
end

local LOG = open_log()

local function log(message)
  local line = string.format("[lua %s] %s\r\n", now(), message)
  if LOG then
    LOG:write(line)
    LOG:flush()
  end
  print(line)
end

local function parse_int(value, default)
  if value == nil or value == "" then
    return default
  end
  local number = tonumber(value)
  if number == nil then
    error("expected a number, got '" .. tostring(value) .. "'")
  end
  return math.floor(number)
end

-- Dump [base, base+length) in blocks. memory.readbyterange returns a 1-based Lua
-- table of bytes; string.char(unpack(...)) keeps the per-call argument count small
-- enough for Lua 5.1's C stack.
local function dump_window(path, base, length)
  local block = 65536
  local chunk = 2048
  local handle, open_error = io.open(path, "wb")
  if not handle then
    error("cannot open dump for writing: " .. tostring(open_error))
  end
  local address = base
  local remaining = length
  local written = 0
  while remaining > 0 do
    local count = math.min(block, remaining)
    local bytes = memory.readbyterange(address, count)
    if bytes == nil then
      handle:close()
      error(string.format("memory.readbyterange failed at 0x%08X", address))
    end
    local index = 1
    while index <= count do
      local last = math.min(index + chunk - 1, count)
      handle:write(string.char(unpack(bytes, index, last)))
      index = last + 1
    end
    written = written + count
    address = address + count
    remaining = remaining - count
  end
  handle:close()
  log(string.format("wrote %d bytes to %s", written, path))
  return written
end

-- Field names DeSmuME 0.9.13 registers for joypad.set (lua-engine.cpp
-- button_mappings): "debug","R","L","X","Y","A","B","start","select","up",
-- "down","left","right","lid". Note the lowercase spellings; an unknown field is
-- silently ignored, so always map through this table.
local BUTTONS = {
  A = true, B = true, X = true, Y = true, L = true, R = true,
  start = true, select = true, up = true, down = true,
  left = true, right = true, debug = true, lid = true,
}

local function canonical_button(name)
  local lower = string.lower(name)
  for candidate in pairs(BUTTONS) do
    if string.lower(candidate) == lower then
      return candidate
    end
  end
  return nil
end

-- Input is injected from a before-emulation callback rather than directly from the
-- script body. DeSmuME only accepts joypad.set() while it is processing user input;
-- a call made from the script's own flow (just after emu.frameadvance) is deferred,
-- and that deferral did not survive in 0.9.13 x64 in testing (joypad.get() stayed
-- empty). LUACALL_BEFOREEMULATION runs inside NDS_beginProcessingInput/
-- NDS_endProcessingInput, so setting the buttons there takes effect on that frame.
local held = {}
local held_touch = { x = 0, y = 0, touch = false }
local function on_before_frame()
  joypad.set(held)
  stylus.set(held_touch)
end

-- Register once; the callback reads `held` every frame.
local registered_before = false
local function ensure_input_callback()
  if not registered_before then
    emu.registerbefore(on_before_frame)
    registered_before = true
  end
end

local function set_buttons(spec)
  ensure_input_callback()
  for name in pairs(held) do
    held[name] = false
  end
  local any = false
  for name in string.gmatch(spec or "", "[^+]+") do
    local canonical = canonical_button(name)
    if canonical == nil then
      error("unknown button in timeline: " .. name)
    end
    held[canonical] = true
    any = true
  end
  return any
end

-- Optional readback so a wrapper can prove the injected state reached the core.
local function log_pad(tag)
  if (os.getenv("DQM_CAPTURE_DEBUG") or "") ~= "1" then
    return
  end
  local names = {}
  local state = joypad.get()
  for name, value in pairs(state) do
    if value then
      names[#names + 1] = name
    end
  end
  table.sort(names)
  log(string.format("pad[%s]=%s frame=%d", tag, table.concat(names, "+"), emu.framecount()))
end

-- A timeline step holds its buttons for FRAMES frames, then releases them.
-- A step with no buttons is an inert wait.
local function run_timeline(timeline)
  if timeline == nil or timeline == "" then
    return
  end
  for step in string.gmatch(timeline, "[^;]+") do
    local frames_text, buttons_text = string.match(step, "^%s*(%d+)%s*:(.*)$")
    if frames_text == nil then
      error("bad timeline step (want FRAMES:BUTTONS): " .. step)
    end
    local frames = tonumber(frames_text)
    local tap_x, tap_y = string.match(buttons_text, "^%s*tap=(%d+),(%d+)$")
    if tap_x then
      -- DS touch-screen tap at DS pixel coordinates, held for the step's frames.
      held_touch.x = tonumber(tap_x)
      held_touch.y = tonumber(tap_y)
      held_touch.touch = true
      for _ = 1, frames do
        emu.frameadvance()
      end
      held_touch.touch = false
      emu.frameadvance()
      log(string.format("timeline tap %d,%d done at frame %d", held_touch.x, held_touch.y,
                        emu.framecount()))
    else
      set_buttons(buttons_text)
      for _ = 1, frames do
        emu.frameadvance()
      end
      log_pad("held")
      set_buttons("")
      emu.frameadvance() -- let the release land before the next step
      log(string.format("timeline step %s done at frame %d", step, emu.framecount()))
    end
  end
end

local function main()
  local out = os.getenv("DQM_CAPTURE_OUT")
  if not out or out == "" then
    error("DQM_CAPTURE_OUT is required")
  end
  local warmup = parse_int(os.getenv("DQM_CAPTURE_FRAMES"), 300)
  local timeline = os.getenv("DQM_CAPTURE_TIMELINE") or ""
  local save_state = parse_int(os.getenv("DQM_CAPTURE_SAVESTATE"), nil)
  local load_state = parse_int(os.getenv("DQM_CAPTURE_LOADSTATE"), nil)

  log(string.format("start frame=%d warmup=%d timeline='%s'", emu.framecount(), warmup, timeline))

  for _ = 1, warmup do
    emu.frameadvance()
  end

  if load_state ~= nil then
    log(string.format("loading state slot %d at frame %d", load_state, emu.framecount()))
    savestate.load(load_state)
    emu.frameadvance()
  end

  run_timeline(timeline)

  if save_state ~= nil then
    log(string.format("saving state slot %d at frame %d", save_state, emu.framecount()))
    savestate.save(save_state)
  end

  log(string.format("dumping at frame %d", emu.framecount()))
  local length = tonumber(os.getenv("DQM_CAPTURE_LENGTH")) or LENGTH
  if length ~= LENGTH then
    log(string.format("full-window override: %d bytes", length))
  end
  dump_window(out, BASE, length)
  log(string.format("dump complete, frame=%d", emu.framecount()))

  if LOG then
    LOG:flush()
    LOG:close()
    LOG = nil
  end

  if (os.getenv("DQM_CAPTURE_PAUSE") or "") == "1" then
    emu.pause()
    return
  end

  if (os.getenv("DQM_CAPTURE_EXIT") or "1") ~= "0" then
    os.exit(0)
  end
end

main()
