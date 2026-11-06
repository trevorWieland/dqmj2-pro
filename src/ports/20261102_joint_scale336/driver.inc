NNSG3dRS *native_data_020ee1f4;
NNSG3dRSOnGlb native_data_020ee1f8;
__declspec(dllimport) void *__stdcall GetStdHandle(u32);
__declspec(dllimport) int __stdcall ReadFile(void *, void *, u32, u32 *, void *);
__declspec(dllimport) int __stdcall WriteFile(void *, const void *, u32, u32 *, void *);
__declspec(dllimport) void *__stdcall VirtualAlloc(void *, u32, u32, u32);
__declspec(dllimport) int __stdcall VirtualFree(void *, u32, u32);
__declspec(dllimport) __declspec(noreturn) void __stdcall ExitProcess(u32);
static void read_exact(void *handle, void *destination, u32 size) {
    u8 *out = destination;
    while (size) {
        u32 count = 0;
        if (!ReadFile(handle, out, size, &count, 0) || !count) ExitProcess(71);
        out += count;
        size -= count;
    }
}
static void write_exact(void *handle, const void *source, u32 size) {
    const u8 *data = source;
    while (size) {
        u32 count = 0;
        if (!WriteFile(handle, data, size, &count, 0) || !count) ExitProcess(72);
        data += count;
        size -= count;
    }
}
void entry(void) {
    void *input = GetStdHandle((u32)-10), *output = GetStdHandle((u32)-11);
    u8 *data = VirtualAlloc((void *)0x02400000, 65536, 0x3000, 4);
    u32 total, index;
    if (data != (void *)0x02400000 || sizeof(void *) != 4 || sizeof(NNSG3dRS) != 392 || sizeof(native_data_020ee1f8) != 11520) ExitProcess(73);
    native_data_020ee1f4 = (NNSG3dRS *)(data + 0x2000);
    read_exact(input, &total, 4);
    if (total > 4096) ExitProcess(74);
    for (index = 0; index < total; ++index) {
        u32 args[4];
        read_exact(input, args, sizeof(args));
        read_exact(input, data, 65536);
        read_exact(input, &native_data_020ee1f8, sizeof(native_data_020ee1f8));
        native_main_0202c84c((NNSG3dJntAnmResult *)args[0], (const fx32 *)args[1], (const u8 *)args[2], args[3]);
        write_exact(output, &index, 4);
        write_exact(output, data, 65536);
        write_exact(output, &native_data_020ee1f8, sizeof(native_data_020ee1f8));
    }
    if (!VirtualFree(data, 0, 0x8000)) ExitProcess(75);
    ExitProcess(0);
}
