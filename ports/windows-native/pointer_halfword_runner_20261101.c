typedef unsigned int u32;
typedef signed int s32;
typedef signed short s16;
typedef unsigned char u8;
typedef void *Handle;

__declspec(dllimport) void __stdcall ExitProcess(u32);
__declspec(dllimport) Handle __stdcall GetStdHandle(u32);
__declspec(dllimport) u32 __stdcall ReadFile(Handle, void *, u32, u32 *, void *);
__declspec(dllimport) u32 __stdcall WriteFile(Handle, const void *, u32, u32 *, void *);
__declspec(dllimport) void *__stdcall VirtualAlloc(void *, u32, u32, u32);

u32 native_arm7_data_03807edc;
extern u32 native_arm7_wram_03801c50(s32, s32, s16);
extern u32 native_arm7_wram_03801c70(s32, s16);
_Static_assert(sizeof(void *) == 4, "Word pointer ABI");
_Static_assert(sizeof(s16) == 2, "Halfword ABI");

static void transfer(Handle handle, void *buffer, u32 length, u32 writing) {
    u32 done;
    u8 *cursor = buffer;
    while (length) {
        done = 0;
        if (writing) {
            if (!WriteFile(handle, cursor, length, &done, 0)) ExitProcess(91);
        } else {
            if (!ReadFile(handle, cursor, length, &done, 0)) ExitProcess(92);
        }
        if (!done || done > length) ExitProcess(93);
        cursor += done;
        length -= done;
    }
}

void j2p_entry(void) {
    Handle input = GetStdHandle((u32)-10);
    Handle output = GetStdHandle((u32)-11);
    u8 *page = VirtualAlloc((void *)0x02380000, 4096, 0x3000, 4);
    u32 count;
    u32 number;
    u32 values[5];
    u32 result;
    if (page != (void *)0x02380000) ExitProcess(94);
    transfer(input, &count, 4, 0);
    if (count > 4096) ExitProcess(95);
    for (number = 0; number < count; number++) {
        transfer(input, values, sizeof(values), 0);
        transfer(input, page, 4096, 0);
        native_arm7_data_03807edc = values[4];
        if (values[0] == 0) {
            result = native_arm7_wram_03801c50((s32)values[1], (s32)values[2], (s16)values[3]);
        } else {
            result = native_arm7_wram_03801c70((s32)values[1], (s16)values[2]);
        }
        transfer(output, &result, 4, 1);
        transfer(output, page, 4096, 1);
    }
    ExitProcess(0);
}
