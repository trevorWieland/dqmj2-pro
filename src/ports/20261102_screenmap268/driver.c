typedef unsigned int u32;
typedef unsigned char u8;
typedef enum NNSG2dTextBGWidth {
    NNS_G2D_TEXT_BG_WIDTH_256 = 32,
    NNS_G2D_TEXT_BG_WIDTH_512 = 64
} NNSG2dTextBGWidth;
typedef enum NNSG2d256x16PlttBGWidth {
    NNS_G2D_256x16PLTT_BG_WIDTH_128 = 16,
    NNS_G2D_256x16PLTT_BG_WIDTH_256 = 32,
    NNS_G2D_256x16PLTT_BG_WIDTH_512 = 64,
    NNS_G2D_256x16PLTT_BG_WIDTH_1024 = 128
} NNSG2d256x16PlttBGWidth;
typedef char pointer_width[(sizeof(void *) == 4) ? 1 : -1];
__declspec(dllimport) void *__stdcall GetStdHandle(u32);
__declspec(dllimport) int __stdcall ReadFile(void *, void *, u32, u32 *, void *);
__declspec(dllimport) int __stdcall WriteFile(void *, const void *, u32, u32 *, void *);
__declspec(dllimport) void *__stdcall VirtualAlloc(void *, u32, u32, u32);
__declspec(dllimport) int __stdcall VirtualFree(void *, u32, u32);
__declspec(dllimport) __declspec(noreturn) void __stdcall ExitProcess(u32);
extern void native_main_020363d0(void *, int, int, int, int, NNSG2dTextBGWidth, int, int);
extern void native_main_02036480(void *, int, int, NNSG2d256x16PlttBGWidth, int, int);

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
    u8 *data = VirtualAlloc((void *)0x02400000, 32768, 0x3000, 4);
    u32 total, index;
    if (data != (void *)0x02400000 || sizeof(unsigned long) != 4) ExitProcess(83);
    read_exact(input, &total, 4);
    if (total > 8192) ExitProcess(84);
    for (index = 0; index < total; ++index) {
        u32 h[9];
        read_exact(input, h, sizeof(h));
        read_exact(input, data, 32768);
        if (h[0] == 0x020363D0)
            native_main_020363d0((void *)h[1], h[2], h[3], h[4], h[5], (NNSG2dTextBGWidth)h[6], h[7], h[8]);
        else if (h[0] == 0x02036480)
            native_main_02036480((void *)h[1], h[2], h[3], (NNSG2d256x16PlttBGWidth)h[4], h[5], h[6]);
        else ExitProcess(85);
        write_exact(output, &index, 4);
        write_exact(output, data, 32768);
    }
    if (!VirtualFree(data, 0, 0x8000)) ExitProcess(86);
    ExitProcess(0);
}
