#include "context.h"
typedef struct { u32 x, y, z; } Vec3;
__declspec(dllimport) void *__stdcall GetStdHandle(u32);
__declspec(dllimport) int __stdcall ReadFile(void *, void *, u32, u32 *, void *);
__declspec(dllimport) int __stdcall WriteFile(void *, const void *, u32, u32 *, void *);
__declspec(dllimport) void *__stdcall VirtualAlloc(void *, u32, u32, u32);
__declspec(dllimport) int __stdcall VirtualFree(void *, u32, u32);
__declspec(dllimport) __declspec(noreturn) void __stdcall ExitProcess(u32);
extern s32 native_ov000_021dbc18(Vec3 *, u8 *, Vec3 *, s32, u8);
u8 portable_global_state[0x7A0];
static u32 notification_count;
static u32 notification_words[4];
static u32 backend_error;
static u32 division_count;
static u32 division_words[2];

void *memcpy(void *destination, const void *source, u32 length) {
    u8 *out = destination;
    const u8 *in = source;
    for (u32 index = 0; index < length; index++) out[index] = in[index];
    return destination;
}

static u64 divide_magnitude(u64 numerator, u32 denominator) {
    u64 quotient = 0;
    u64 remainder = 0;
    for (s32 index = 0; index < 64; index++) {
        remainder = (remainder << 1) | (numerator >> 63);
        numerator <<= 1;
        quotient <<= 1;
        if (remainder >= denominator) {
            remainder -= denominator;
            quotient |= 1;
        }
    }
    return quotient;
}

u32 native_fn_0200235c(u32 numerator, s32 denominator) {
    division_count++;
    division_words[0] = numerator;
    division_words[1] = (u32) denominator;
    s64 signed_numerator = (s64) (s32) numerator * 0x100000000LL;
    u64 magnitude;
    u32 divisor;
    u64 quotient;
    if (denominator == 0) {
        backend_error = 1;
        return 0;
    }
    magnitude = signed_numerator < 0 ? 0ULL - (u64) signed_numerator : (u64) signed_numerator;
    divisor = denominator < 0 ? 0U - (u32) denominator : (u32) denominator;
    quotient = divide_magnitude(magnitude, divisor);
    if ((signed_numerator < 0) != (denominator < 0)) quotient = 0ULL - quotient;
    return (u32) ((quotient + 0x80000ULL) >> 20);
}

u32 native_fn_ov000_021dbbb8(void *context, void *point) {
    backend_error = 2;
    return 0;
}

u32 native_fn_ov000_021da57c(void *context, s32 index, void *triangle, u32 mesh) {
    notification_count++;
    notification_words[0] = (u32) context;
    notification_words[1] = (u32) index;
    notification_words[2] = (u32) triangle;
    notification_words[3] = mesh;
    return 0xA5123456;
}

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
    void *input = GetStdHandle((u32) -10);
    void *output = GetStdHandle((u32) -11);
    u8 *page = VirtualAlloc((void *) 0x02500000, 4096, 0x3000, 4);
    u32 total;
    if (page != (void *) 0x02500000) ExitProcess(83);
    read_exact(input, &total, 4);
    if (total > 4096) ExitProcess(84);
    for (u32 ordinal = 0; ordinal < total; ordinal++) {
        u32 header[13];
        u8 *mesh = page;
        Vec3 *point = (Vec3 *) (page + 0x200);
        u8 *context = page + 0x220;
        Vec3 *out = (Vec3 *) (page + 0x240);
        u32 result[14];
        read_exact(input, header, sizeof(header));
        read_exact(input, page, 4096);
        *(u32 *) (portable_global_state + 0x79C) = (u32) mesh;
        notification_count = 0;
        backend_error = 0;
        division_count = 0;
        division_words[0] = division_words[1] = 0;
        for (u32 index = 0; index < 4; index++) notification_words[index] = 0;
        result[0] = ordinal;
        result[1] = (u32) native_ov000_021dbc18(point, context, header[11] ? 0 : out, 0, (u8) header[9]);
        result[2] = out->x;
        result[3] = out->y;
        result[4] = out->z;
        result[5] = notification_count;
        for (u32 index = 0; index < 4; index++) result[6 + index] = notification_words[index];
        result[10] = backend_error;
        result[11] = division_count;
        result[12] = division_words[0];
        result[13] = division_words[1];
        write_exact(output, result, sizeof(result));
        write_exact(output, page, 4096);
    }
    if (!VirtualFree(page, 0, 0x8000)) ExitProcess(85);
    ExitProcess(0);
}
