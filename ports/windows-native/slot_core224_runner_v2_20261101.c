typedef unsigned int u32;
typedef unsigned char u8;
typedef void *Handle;

__declspec(dllimport) void __stdcall ExitProcess(u32);
__declspec(dllimport) Handle __stdcall GetStdHandle(u32);
__declspec(dllimport) u32 __stdcall ReadFile(Handle, void *, u32, u32 *, void *);
__declspec(dllimport) u32 __stdcall WriteFile(Handle, const void *, u32, u32 *, void *);
__declspec(dllimport) void *__stdcall VirtualAlloc(void *, u32, u32, u32);

#include "../../src/runtime/20261101_slot_core152/state.h"
#include "../../src/runtime/runtime03/native_main_020388dc.c"

__declspec(align(4)) u8 native_data_020f4c38[12];
extern u32 native_main_0203b5d8(State *, s32, const u8 *);
extern u32 native_main_0203a650(State *, s32, const u8 *);

_Static_assert(sizeof(void *) == 4, "32-bit ABI");
_Static_assert(__builtin_offsetof(State, mask) == 0x44, "mask");
_Static_assert(__builtin_offsetof(State, count) == 0x48, "count");
_Static_assert(__builtin_offsetof(State, slots) == 0x4C, "slots");
_Static_assert(__builtin_offsetof(State, references) == 0x120, "references");

static u32 indexValue;
static u32 provided;
static u32 commandWord;
static u32 commandZero;

u32 native_fn_020388dc(u32 mask) {
    return native_main_020388dc((s32)mask);
}

u32 native_fn_020092a4(s32 word, s32 zero) {
    provided++;
    commandWord = (u32)word;
    commandZero = (u32)zero;
    return 0xF13579BDU + indexValue;
}

static void transfer(Handle handle, void *buffer, u32 length, u32 writing) {
    u32 done;
    u8 *bytes = buffer;
    while (length) {
        done = 0;
        if (writing) {
            if (!WriteFile(handle, bytes, length, &done, 0)) ExitProcess(81);
        } else {
            if (!ReadFile(handle, bytes, length, &done, 0)) ExitProcess(82);
        }
        if (!done || done > length) ExitProcess(83);
        bytes += done;
        length -= done;
    }
}

void j2p_entry(void) {
    Handle input = GetStdHandle((u32)-10);
    Handle output = GetStdHandle((u32)-11);
    u8 *page = VirtualAlloc((void *)0x02380000, 4096, 0x3000, 4);
    u8 *globalRegion = VirtualAlloc((void *)0x020F0000, 65536, 0x3000, 4);
    u8 *globalPage = (u8 *)0x020F4000;
    u32 count;
    u32 number;
    u32 slot;
    u32 header[5];
    u32 results[4];
    if (page != (void *)0x02380000 || globalRegion != (void *)0x020F0000) ExitProcess(84);
    transfer(input, &count, 4, 0);
    if (count > 2048) ExitProcess(85);
    for (number = 0; number < count; number++) {
        transfer(input, header, sizeof(header), 0);
        transfer(input, page, 4096, 0);
        transfer(input, globalPage, 4096, 0);
        for (slot = 0; slot < 12; slot++) native_data_020f4c38[slot] = globalPage[0xC38 + slot];
        indexValue = header[1];
        provided = commandWord = commandZero = 0;
        if (header[0] == 0) {
            results[0] = native_main_0203b5d8((State *)header[2], (s32)header[3], (const u8 *)header[4]);
        } else {
            results[0] = native_main_0203a650((State *)header[2], (s32)header[3], (const u8 *)header[4]);
        }
        for (slot = 0; slot < 12; slot++) globalPage[0xC38 + slot] = native_data_020f4c38[slot];
        results[1] = provided;
        results[2] = commandWord;
        results[3] = commandZero;
        transfer(output, results, sizeof(results), 1);
        transfer(output, page, 4096, 1);
        transfer(output, globalPage, 4096, 1);
    }
    ExitProcess(0);
}
