typedef unsigned char u8;
typedef unsigned int u32;
typedef struct {
    u32 action, argc, args[3], value, before_error, after_error;
    u8 before[72], after[72];
} AsyncEvent;
typedef struct {
    u32 path, buffer, length, offset, old_error, result, error, count, use_default;
    u8 initial[84], expected[84];
    AsyncEvent events[3];
} AsyncCase;
#include "async_acceptance_vectors.h"

_Alignas(4) u8 native_data_020edecc[84];
u32 native_data_020edec8;
static _Alignas(4) u8 explicit_context[84];
static const AsyncCase *active_case;
static u8 *active_context;
static u32 event_index, failed, cases_done, provider_calls;
extern u32 native_main_0202a954(u8 *, u32, u32, u32, u32);

static void copy_bytes(u8 *to, const u8 *from, u32 size) {
    u32 i;
    for (i = 0; i < size; ++i) to[i] = from[i];
}

static u32 equal_bytes(const u8 *a, const u8 *b, u32 size) {
    u32 i;
    for (i = 0; i < size; ++i) if (a[i] != b[i]) return 0;
    return 1;
}

static u32 service(u32 action, void *file, u32 arg1, u32 arg2) {
    const AsyncEvent *event;
    if (event_index >= active_case->count || event_index >= 3) {
        failed = 1;
        return 0;
    }
    event = &active_case->events[event_index++];
    ++provider_calls;
    if (event->action != action || file != active_context + 12 ||
        arg1 != event->args[1] || (event->argc == 3 && arg2 != event->args[2]) ||
        native_data_020edec8 != event->before_error ||
        !equal_bytes((const u8 *)file, event->before, 72)) failed = 1;
    copy_bytes((u8 *)file, event->after, 72);
    native_data_020edec8 = event->after_error;
    return event->value;
}

u32 native_fn_0200bfe4(void *file, u32 path) {
    return service(0, file, path, 0);
}

u32 native_fn_0200c190(void *file, u32 offset, u32 origin) {
    return service(1, file, offset, origin);
}

u32 native_fn_0200c170(void *file, u32 destination, u32 size) {
    return service(2, file, destination, size);
}

u32 j2p_async_run_all(void) {
    u32 i, result;
    cases_done = provider_calls = failed = 0;
    for (i = 0; i < ASYNC_CASE_COUNT; ++i) {
        active_case = &async_cases[i];
        active_context = active_case->use_default ? native_data_020edecc : explicit_context;
        copy_bytes(active_context, active_case->initial, 84);
        native_data_020edec8 = active_case->old_error;
        event_index = 0;
        result = native_main_0202a954(active_case->use_default ? (u8 *)0 : active_context,
            active_case->path, active_case->buffer, active_case->length, active_case->offset);
        if (result != active_case->result || native_data_020edec8 != active_case->error ||
            event_index != active_case->count || !equal_bytes(active_context, active_case->expected, 84)) failed = 1;
        ++cases_done;
        if (failed) return i + 1;
    }
    return 0;
}

u32 j2p_async_cases_done(void) { return cases_done; }
u32 j2p_async_provider_calls(void) { return provider_calls; }
