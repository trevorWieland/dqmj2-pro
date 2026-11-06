typedef unsigned int u32;
typedef unsigned char u8;
typedef void *Handle;

__declspec(dllimport) void __stdcall ExitProcess(u32);
__declspec(dllimport) Handle __stdcall GetStdHandle(u32);
__declspec(dllimport) u32 __stdcall ReadFile(Handle, void *, u32, u32 *, void *);
__declspec(dllimport) u32 __stdcall WriteFile(Handle, const void *, u32, u32 *, void *);
__declspec(dllimport) void *__stdcall VirtualAlloc(void *, u32, u32, u32);

#include "../../src/runtime/20261101_callback_cursor192/native_main_0200a81c.c"

_Static_assert(sizeof(void *) == 4, "32-bit ABI required");
_Static_assert(__builtin_offsetof(State, flags) == 0x1C, "flags");
_Static_assert(__builtin_offsetof(State, result) == 0x24, "result");
_Static_assert(__builtin_offsetof(State, operation) == 0x50, "operation");
_Static_assert(__builtin_offsetof(Cursor, offset) == 4, "offset");
_Static_assert(__builtin_offsetof(Result, status) == 0x14, "status");

typedef struct {
    u32 index;
    u32 cursor;
    u32 value;
    u32 length;
    u32 irq;
    u32 status;
    u32 waits;
    u32 callbackFlags;
    u32 replacement;
    u32 finalStatus;
} Input;

static Input input;
static Cursor *cursor;
static State *state;
static u32 irqState;
static u32 callbacks;
static u32 sleeps;
static u32 disables;
static u32 restores;
static u32 errors;

static void transfer(Handle handle, void *buffer, u32 length, u32 writing) {
    u32 done;
    u8 *bytes = buffer;
    while (length != 0) {
        done = 0;
        if (writing) {
            if (!WriteFile(handle, bytes, length, &done, 0)) ExitProcess(71);
        } else {
            if (!ReadFile(handle, bytes, length, &done, 0)) ExitProcess(72);
        }
        if (!done || done > length) ExitProcess(73);
        bytes += done;
        length -= done;
    }
}

u32 native_fn_02007ff4(void) {
    u32 before = irqState;
    irqState = 0x80;
    disables++;
    return before;
}

u32 native_fn_02008008(u32 previous) {
    u32 before = irqState;
    irqState = previous & 0x80;
    restores++;
    return before;
}

void native_fn_020068d4(void *queue) {
    sleeps++;
    if (queue != (u8 *)state + 0xC || irqState != 0x80 || sleeps > 3) ExitProcess(74);
    cursor->offset = input.replacement + sleeps * 0x10001;
    if (sleeps == input.waits) {
        state->flags = input.callbackFlags & ~0x200U;
        ((Result *)0x02380700)->status = input.finalStatus ^ (sleeps << 24);
    }
}

static u32 operation(State *actual, u32 value, u32 offset, u32 length) {
    callbacks++;
    if (actual != state || value != input.value || offset != cursor->offset || length != input.length) errors++;
    if (!(state->flags & 0x200)) errors++;
    state->flags = input.callbackFlags;
    state->result = (Result *)0x02380700;
    if (input.index % 3 == 0) cursor->offset = input.replacement;
    return input.status;
}

void j2p_entry(void) {
    Handle standardInput = GetStdHandle((u32)-10);
    Handle standardOutput = GetStdHandle((u32)-11);
    u8 *page = VirtualAlloc((void *)0x02380000, 4096, 0x3000, 4);
    u32 count;
    u32 number;
    u32 output[7];
    if (page != (void *)0x02380000) ExitProcess(75);
    transfer(standardInput, &count, 4, 0);
    if (count > 4096) ExitProcess(76);
    for (number = 0; number < count; number++) {
        transfer(standardInput, &input, sizeof(input), 0);
        transfer(standardInput, page, 4096, 0);
        cursor = (Cursor *)input.cursor;
        state = cursor->state;
        state->operation = operation;
        irqState = input.irq;
        callbacks = sleeps = disables = restores = errors = 0;
        output[0] = native_main_0200a81c(cursor, input.value, input.length);
        output[1] = irqState;
        output[2] = callbacks;
        output[3] = sleeps;
        output[4] = disables;
        output[5] = restores;
        output[6] = errors;
        state->operation = (Operation)0x026A0000;
        transfer(standardOutput, output, sizeof(output), 1);
        transfer(standardOutput, page, 4096, 1);
    }
    ExitProcess(0);
}
