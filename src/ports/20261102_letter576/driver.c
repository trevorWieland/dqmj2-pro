typedef unsigned int u32;
typedef unsigned char u8;
typedef struct LC_INFO LC_INFO;
typedef char pointer_width[(sizeof(void *) == 4) ? 1 : -1];
__declspec(dllimport) void *__stdcall GetStdHandle(u32);
__declspec(dllimport) int __stdcall ReadFile(void *, void *, u32, u32 *, void *);
__declspec(dllimport) int __stdcall WriteFile(void *, const void *, u32, u32 *, void *);
__declspec(dllimport) void *__stdcall VirtualAlloc(void *, u32, u32, u32);
__declspec(dllimport) int __stdcall VirtualFree(void *, u32, u32);
__declspec(dllimport) __declspec(noreturn) void __stdcall ExitProcess(u32);
extern void native_main_02035788(LC_INFO *);

static void read_exact(void *handle, void *destination, u32 size) {
    u8 *out = destination;
    while (size) {
        u32 count = 0;
        if (!ReadFile(handle, out, size, &count, 0) || !count) ExitProcess(81);
        out += count;
        size -= count;
    }
}

static void write_exact(void *handle, const void *source, u32 size) {
    const u8 *data = source;
    while (size) {
        u32 count = 0;
        if (!WriteFile(handle, data, size, &count, 0) || !count) ExitProcess(82);
        data += count;
        size -= count;
    }
}

void entry(void) {
    void *input = GetStdHandle((u32)-10), *output = GetStdHandle((u32)-11);
    u8 *data = VirtualAlloc((void *)0x02400000, 16384, 0x3000, 4);
    u32 total, index;
    if (data != (void *)0x02400000 || sizeof(unsigned long) != 4) ExitProcess(83);
    read_exact(input, &total, 4);
    if (total > 8192) ExitProcess(84);
    for (index = 0; index < total; ++index) {
        u32 header[2];
        read_exact(input, header, sizeof(header));
        read_exact(input, data, 16384);
        if (header[0] != 0x02035788) ExitProcess(85);
        native_main_02035788((LC_INFO *)header[1]);
        write_exact(output, &index, 4);
        write_exact(output, data, 16384);
    }
    if (!VirtualFree(data, 0, 0x8000)) ExitProcess(86);
    ExitProcess(0);
}
