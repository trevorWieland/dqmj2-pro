typedef unsigned int u32;
typedef unsigned char u8;
typedef void *Handle;
#include "random_word152_record_20261101.h"

__declspec(dllimport) void __stdcall ExitProcess(u32);
__declspec(dllimport) Handle __stdcall GetStdHandle(u32);
__declspec(dllimport) u32 __stdcall ReadFile(Handle, void *, u32, u32 *, void *);
__declspec(dllimport) u32 __stdcall WriteFile(Handle, const void *, u32, u32 *, void *);

u32 native_rng_state;
J2pRandomWordRecord native_data_020f6028;
extern u32 native_main_0203d158(u32);
extern u32 native_main_0203d1f0(void);
_Static_assert(sizeof(u32) == 4 && sizeof(void *) == 4, "Word ABI");

static void transfer(Handle handle, void *buffer, u32 remaining, u32 writing) {
    u32 done;
    u8 *cursor = buffer;
    while (remaining) {
        done = 0;
        if (writing) {
            if (!WriteFile(handle, cursor, remaining, &done, 0)) ExitProcess(91);
        } else {
            if (!ReadFile(handle, cursor, remaining, &done, 0)) ExitProcess(92);
        }
        if (!done || done > remaining) ExitProcess(93);
        cursor += done;
        remaining -= done;
    }
}

void j2p_entry(void) {
    Handle input = GetStdHandle((u32)-10);
    Handle output = GetStdHandle((u32)-11);
    u32 count;
    u32 index;
    u32 arguments[2];
    u32 results[3];
    if ((u32)&native_data_020f6028 & 3) ExitProcess(94);
    transfer(input, &count, 4, 0);
    if (count > 4096) ExitProcess(95);
    for (index = 0; index < count; index++) {
        transfer(input, arguments, sizeof(arguments), 0);
        transfer(input, &native_data_020f6028, sizeof(native_data_020f6028), 0);
        native_rng_state = arguments[0];
        results[0] = native_main_0203d158(arguments[1]);
        results[1] = native_rng_state;
        results[2] = native_main_0203d1f0();
        transfer(output, results, sizeof(results), 1);
        transfer(output, &native_data_020f6028, sizeof(native_data_020f6028), 1);
    }
    ExitProcess(0);
}
