#include "../../src/arm7/20261101_bitfields544/native_fields.h"
typedef unsigned char u8;
typedef void *Handle;

__declspec(dllimport) void __stdcall ExitProcess(u32);
__declspec(dllimport) Handle __stdcall GetStdHandle(u32);
__declspec(dllimport) u32 __stdcall ReadFile(Handle, void *, u32, u32 *, void *);
__declspec(dllimport) u32 __stdcall WriteFile(Handle, const void *, u32, u32 *, void *);
__declspec(dllimport) void *__stdcall VirtualAlloc(void *, u32, u32, u32);
__declspec(dllimport) u32 __stdcall VirtualProtect(void *, u32, u32, u32 *);
extern u32 native_arm7_main_027f6ca0(u32);
extern u32 native_arm7_main_027f6db0(u32);
_Static_assert(sizeof(PackedFields) == 4, "Measured word view");
_Static_assert(sizeof(void *) == 4, "Word pointer ABI");

static void transfer(Handle handle, void *buffer, u32 size, u32 writing) {
    u8 *cursor = buffer;
    u32 done;
    while (size) {
        done = 0;
        if (writing) {
            if (!WriteFile(handle, cursor, size, &done, 0)) ExitProcess(91);
        } else {
            if (!ReadFile(handle, cursor, size, &done, 0)) ExitProcess(92);
        }
        if (!done || done > size) ExitProcess(93);
        cursor += done;
        size -= done;
    }
}

void j2p_entry(void) {
    Handle input = GetStdHandle((u32)-10);
    Handle output = GetStdHandle((u32)-11);
    u8 *page = VirtualAlloc((void *)0x03040000, 4096, 0x3000, 4);
    u32 count;
    u32 number;
    u32 values[3];
    u32 previous;
    u32 result;
    u32 pointer;
    if (page != (void *)0x03040000) ExitProcess(94);
    transfer(input, &count, 4, 0);
    if (count > 4096) ExitProcess(95);
    for (number = 0; number < count; number++) {
        transfer(input, values, sizeof(values), 0);
        if (values[0] > 1 || values[1] > 4092 || values[1] & 3 || values[2] > 1) ExitProcess(96);
        transfer(input, page, 4096, 0);
        pointer = (u32)(page + values[1]);
        if (values[2] && !VirtualProtect(page, 4096, 2, &previous)) ExitProcess(97);
        if (values[0]) result = native_arm7_main_027f6db0(pointer);
        else result = native_arm7_main_027f6ca0(pointer);
        if (values[2] && !VirtualProtect(page, 4096, 4, &previous)) ExitProcess(98);
        transfer(output, &result, 4, 1);
        transfer(output, page, 4096, 1);
    }
    ExitProcess(0);
}
