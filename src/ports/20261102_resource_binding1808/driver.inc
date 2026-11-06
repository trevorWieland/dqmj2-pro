__declspec(dllimport) void *__stdcall GetStdHandle(u32);
__declspec(dllimport) int __stdcall ReadFile(void *, void *, u32, u32 *, void *);
__declspec(dllimport) int __stdcall WriteFile(void *, const void *, u32, u32 *, void *);
__declspec(dllimport) void *__stdcall VirtualAlloc(void *, u32, u32, u32);
__declspec(dllimport) int __stdcall VirtualFree(void *, u32, u32);
__declspec(dllimport) __declspec(noreturn) void __stdcall ExitProcess(u32);
typedef unsigned long long u64;
typedef struct NNSG3dResMdl_ NNSG3dResMdl;
typedef struct NNSG3dResMat_ NNSG3dResMat;
typedef struct NNSG3dResDictTexToMatIdxData_ NNSG3dResDictTexToMatIdxData;
typedef struct NNSG3dResDictPlttToMatIdxData_ NNSG3dResDictPlttToMatIdxData;
typedef struct NNSG3dResDictTexData_ NNSG3dResDictTexData;
typedef struct NNSG3dResDictPlttData_ NNSG3dResDictPlttData;
extern BOOL native_main_0202f3dc(NNSG3dResMdlSet *, const NNSG3dResTex *);
extern BOOL native_main_0202efe4(NNSG3dResMdl *, const NNSG3dResTex *);
extern BOOL native_main_0202f250(NNSG3dResMdl *, const NNSG3dResTex *);
extern void native_main_0202edfc(NNSG3dResMat *, NNSG3dResDictTexToMatIdxData *, const NNSG3dResTex *, const NNSG3dResDictTexData *);
extern void native_main_0202f170(NNSG3dResMat *, NNSG3dResDictPlttToMatIdxData *, const NNSG3dResTex *, const NNSG3dResDictPlttData *);
extern u32 native_main_02002458(u32, s32);
typedef struct { u32 entry, count, words[3]; } BackendCall;
static BackendCall calls[16];
static u32 call_count, division_count, failed, keys[3];
static void record(u32 entry, u32 count, u32 a, u32 b, u32 c) {
    BackendCall *p;
    if (call_count >= 16 || count > 3) ExitProcess(81);
    p = calls + call_count++;
    p->entry = entry;
    p->count = count;
    p->words[0] = a;
    p->words[1] = b;
    p->words[2] = c;
}
static u32 alloc_tex(u32 size, BOOL compressed, u32 options) {
    if ((u32)compressed > 1) ExitProcess(82);
    record(0x0F000100, 3, size, (u32)compressed, options);
    return (failed & (1U << compressed)) ? 0 : keys[compressed];
}
static u32 alloc_palette(u32 size, BOOL four, u32 options) {
    record(0x0F000120, 3, size, (u32)four, options);
    return (failed & 4) ? 0 : keys[2];
}
static int free_tex(u32 key) {
    record(0x0F000110, 1, key, 0, 0);
    return (int)(0xD00D0000U + call_count);
}
static int free_palette(u32 key) {
    record(0x0F000130, 1, key, 0, 0);
    return (int)(0xD00D0000U + call_count);
}
NNSGfdFuncAllocTexVram native_data_020dd8c0 = alloc_tex;
NNSGfdFuncFreeTexVram native_data_020dd8c4 = free_tex;
NNSGfdFuncAllocPlttVram native_data_020dd8b8 = alloc_palette;
NNSGfdFuncFreePlttVram native_data_020dd8bc = free_palette;
void native_fn_0202ec6c(void *tex, s32 begin_end) { record(0x0202EC6C, 2, (u32)tex, (u32)begin_end, 0); }
void native_fn_0202ed8c(void *tex, s32 begin_end) { record(0x0202ED8C, 2, (u32)tex, (u32)begin_end, 0); }
u32 resource_hardware_divide_setup(u32 numerator, s32 denominator) {
    u32 result = native_main_02002458(numerator, denominator);
    volatile u16 *control = (volatile u16 *)0x04000280;
    volatile u64 *operand = (volatile u64 *)0x04000290;
    volatile s32 *divisor = (volatile s32 *)0x04000298;
    volatile u64 *output = (volatile u64 *)0x040002A0;
    u64 input = *operand, remainder = 0, quotient = 0;
    u32 i;
    if (*control != 1 || denominator <= 0 || *divisor != denominator ||
        input != ((u64)numerator << 32) || (input >> 63)) ExitProcess(83);
    for (i = 0; i < 64; ++i) {
        remainder = (remainder << 1) | (input >> 63);
        input <<= 1;
        quotient <<= 1;
        if (remainder >= (u32)denominator) {
            remainder -= (u32)denominator;
            quotient |= 1;
        }
    }
    output[0] = quotient;
    output[1] = remainder;
    *control = 1;
    ++division_count;
    return result;
}
static void read_exact(void *handle, void *destination, u32 size) {
    u8 *out = destination;
    while (size) {
        u32 count = 0;
        if (!ReadFile(handle, out, size, &count, 0) || !count) ExitProcess(84);
        out += count;
        size -= count;
    }
}
static void write_exact(void *handle, const void *source, u32 size) {
    const u8 *data = source;
    while (size) {
        u32 count = 0;
        if (!WriteFile(handle, data, size, &count, 0) || !count) ExitProcess(85);
        data += count;
        size -= count;
    }
}
void entry(void) {
    void *input = GetStdHandle((u32)-10), *output = GetStdHandle((u32)-11);
    u8 *data = VirtualAlloc((void *)0x02400000, 65536, 0x3000, 4);
    u8 *hardware = VirtualAlloc((void *)0x04000000, 4096, 0x3000, 4);
    u32 total, index;
    if (data != (void *)0x02400000 || hardware != (void *)0x04000000 || sizeof(void *) != 4) ExitProcess(86);
    read_exact(input, &total, 4);
    if (total > 8192) ExitProcess(87);
    for (index = 0; index < total; ++index) {
        u32 header[9], result = 0, metadata[4], i;
        read_exact(input, header, sizeof(header));
        read_exact(input, data, 65536);
        failed = header[5];
        keys[0] = header[6];keys[1] = header[7];keys[2] = header[8];
        call_count = division_count = 0;
        switch (header[0]) {
        case 0x02031FA4: result = (u32)native_main_02031fa4((void *)header[1]);break;
        case 0x0202F3DC: result = (u32)native_main_0202f3dc((NNSG3dResMdlSet *)header[1], (NNSG3dResTex *)header[2]);break;
        case 0x0202EFE4: result = (u32)native_main_0202efe4((NNSG3dResMdl *)header[1], (NNSG3dResTex *)header[2]);break;
        case 0x0202F250: result = (u32)native_main_0202f250((NNSG3dResMdl *)header[1], (NNSG3dResTex *)header[2]);break;
        case 0x0202EDFC: native_main_0202edfc((NNSG3dResMat *)header[1], (NNSG3dResDictTexToMatIdxData *)header[2], (NNSG3dResTex *)header[3], (NNSG3dResDictTexData *)header[4]);break;
        case 0x0202F170: native_main_0202f170((NNSG3dResMat *)header[1], (NNSG3dResDictPlttToMatIdxData *)header[2], (NNSG3dResTex *)header[3], (NNSG3dResDictPlttData *)header[4]);break;
        default: ExitProcess(88);
        }
        metadata[0] = index;metadata[1] = result;metadata[2] = call_count;metadata[3] = division_count;
        write_exact(output, metadata, sizeof(metadata));
        for (i = 0; i < call_count; ++i) write_exact(output, calls + i, (2 + calls[i].count) * 4);
        write_exact(output, data, 65536);
    }
    if (!VirtualFree(data, 0, 0x8000) || !VirtualFree(hardware, 0, 0x8000)) ExitProcess(89);
    ExitProcess(0);
}
