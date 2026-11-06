typedef unsigned long u32;
typedef unsigned short u16;
typedef unsigned char u8;
typedef struct NNSG3dResMatCAnm_ NNSG3dResMatCAnm;
typedef struct NNSG3dResTexSRTAnm_ NNSG3dResTexSRTAnm;
typedef char pointer_width[(sizeof(void *) == 4 && sizeof(u32) == 4) ? 1 : -1];
__declspec(dllimport) void *__stdcall GetStdHandle(u32);
__declspec(dllimport) int __stdcall ReadFile(void *, void *, u32, u32 *, void *);
__declspec(dllimport) int __stdcall WriteFile(void *, const void *, u32, u32 *, void *);
__declspec(dllimport) void *__stdcall VirtualAlloc(void *, u32, u32, u32);
__declspec(dllimport) int __stdcall VirtualFree(void *, u32, u32);
__declspec(dllimport) __declspec(noreturn) void __stdcall ExitProcess(u32);
extern u16 native_main_02033930(const NNSG3dResMatCAnm *, u32, u32);
extern u16 native_main_02033a98(const NNSG3dResMatCAnm *, u32, u32);
extern int native_main_02033d48(const NNSG3dResTexSRTAnm *, u32, u32, u32);
extern u32 native_main_02033e48(const NNSG3dResTexSRTAnm *, u32, u32, u32);

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
    if (data != (void *)0x02400000) ExitProcess(83);
    read_exact(input, &total, 4);
    if (total > 8192) ExitProcess(84);
    for (index = 0; index < total; ++index) {
        u32 h[5], result;
        read_exact(input, h, sizeof(h));
        read_exact(input, data, 16384);
        switch (h[0]) {
        case 0x02033930: result = native_main_02033930((void *)h[1], h[2], h[3]);break;
        case 0x02033A98: result = native_main_02033a98((void *)h[1], h[2], h[3]);break;
        case 0x02033D48: result = (u32)native_main_02033d48((void *)h[1], h[2], h[3], h[4]);break;
        case 0x02033E48: result = native_main_02033e48((void *)h[1], h[2], h[3], h[4]);break;
        default: ExitProcess(85);
        }
        write_exact(output, &index, 4);
        write_exact(output, &result, 4);
        write_exact(output, data, 16384);
    }
    if (!VirtualFree(data, 0, 0x8000)) ExitProcess(86);
    ExitProcess(0);
}
