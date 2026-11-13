typedef unsigned int u32;
typedef unsigned short u16;
typedef unsigned char u8;
struct NNSG3dAnmObj_;
struct NNSG3dResMdl_;
struct NNSG3dMatAnmResult_;
struct NNSG3dJntAnmResult_;
struct NNSG3dVisAnmResult_;
typedef void (*Init)(struct NNSG3dAnmObj_ *, void *, const struct NNSG3dResMdl_ *);
typedef void (*Mat)(struct NNSG3dMatAnmResult_ *, const struct NNSG3dAnmObj_ *, u32);
typedef void (*Joint)(struct NNSG3dJntAnmResult_ *, const struct NNSG3dAnmObj_ *, u32);
typedef void (*Vis)(struct NNSG3dVisAnmResult_ *, const struct NNSG3dAnmObj_ *, u32);
typedef struct { u8 category0, dummy_; u16 category1; Init func; } Record;
u32 native_data_020dd5f4;
Record native_data_020dd618[10];
/* Measured data order: 020dd5f8, 020dd5fc, 020dd600, 020dd604, 020dd608.
   MWCC emits reverse(declaration[:-1]) + last, so declare in this order. */
Mat native_data_020dd604 = (Mat)0x02034388;
Mat native_data_020dd600 = (Mat)0x02034128;
Joint native_data_020dd5fc = (Joint)0x020323A0;
Vis native_data_020dd5f8 = (Vis)0x02034448;
Mat native_data_020dd608 = (Mat)0x02033C58;
extern void native_main_0202e8b8(u32 object, u32 animation, int model, u32 texture);
extern void native_main_02033b84(struct NNSG3dAnmObj_ *, void *, const struct NNSG3dResMdl_ *);
extern void native_main_0203416c(struct NNSG3dAnmObj_ *, void *, const struct NNSG3dResMdl_ *);
extern void native_main_02034054(struct NNSG3dAnmObj_ *, void *, const struct NNSG3dResMdl_ *);
extern void native_main_020343fc(struct NNSG3dAnmObj_ *, void *, const struct NNSG3dResMdl_ *);
extern void native_main_02032324(struct NNSG3dAnmObj_ *, void *, const struct NNSG3dResMdl_ *);
extern u32 selected_dictionary_index(int dictionary, u8 *name);
__declspec(dllimport) void *__stdcall GetStdHandle(u32);
__declspec(dllimport) int __stdcall ReadFile(void *, void *, u32, u32 *, void *);
__declspec(dllimport) int __stdcall WriteFile(void *, const void *, u32, u32 *, void *);
__declspec(dllimport) void *__stdcall VirtualAlloc(void *, u32, u32, u32);
__declspec(dllimport) int __stdcall VirtualFree(void *, u32, u32);
__declspec(dllimport) __declspec(noreturn) void __stdcall ExitProcess(u32);
static u32 fill_count, dictionary_count;
void native_fn_02008be0(u16 data, void *destination, u32 size) {
    u16 *out = destination;
    u32 i;
    ++fill_count;
    for (i = 0; i < size / 2; ++i) out[i] = data;
}
u32 native_fn_0202bd74(int dictionary, u8 *name) {
    ++dictionary_count;
    return selected_dictionary_index(dictionary, name);
}
static Init translate(u32 address) {
    switch (address) {
    case 0: return 0;
    case 0x02033B84: return native_main_02033b84;
    case 0x0203416C: return native_main_0203416c;
    case 0x02034054: return native_main_02034054;
    case 0x020343FC: return native_main_020343fc;
    case 0x02032324: return native_main_02032324;
    }
    ExitProcess(61);
}
static void read_exact(void *handle, void *destination, u32 size) {
    u8 *out = destination;
    while (size) {
        u32 read = 0;
        if (!ReadFile(handle, out, size, &read, 0) || !read) ExitProcess(62);
        out += read;
        size -= read;
    }
}
static void write_exact(void *handle, const void *source, u32 size) {
    const u8 *data = source;
    while (size) {
        u32 written = 0;
        if (!WriteFile(handle, data, size, &written, 0) || !written) ExitProcess(63);
        data += written;
        size -= written;
    }
}
void entry(void) {
    void *input = GetStdHandle((u32)-10), *output = GetStdHandle((u32)-11);
    u8 *data = VirtualAlloc((void *)0x02400000, 65536, 0x3000, 4);
    u32 total, index;
    if (sizeof(void *) != 4 || sizeof(Record) != 8 || data != (void *)0x02400000) ExitProcess(64);
    read_exact(input, &total, 4);
    if (total > 4096) ExitProcess(65);
    for (index = 0; index < total; ++index) {
        u32 words[6], raw[20], result[3], i;
        read_exact(input, words, sizeof(words));
        read_exact(input, raw, sizeof(raw));
        read_exact(input, data, 65536);
        if (words[0] != index || words[1] > 10) ExitProcess(66);
        native_data_020dd5f4 = words[1];
        for (i = 0; i < 10; ++i) {
            native_data_020dd618[i].category0 = (u8)raw[i * 2];
            native_data_020dd618[i].dummy_ = (u8)(raw[i * 2] >> 8);
            native_data_020dd618[i].category1 = (u16)(raw[i * 2] >> 16);
            native_data_020dd618[i].func = translate(raw[i * 2 + 1]);
        }
        fill_count = dictionary_count = 0;
        native_main_0202e8b8(words[2], words[3], (int)words[4], words[5]);
        result[0] = index;
        result[1] = fill_count;
        result[2] = dictionary_count;
        write_exact(output, result, sizeof(result));
        write_exact(output, data, 65536);
    }
    if (!VirtualFree(data, 0, 0x8000)) ExitProcess(67);
    ExitProcess(0);
}
