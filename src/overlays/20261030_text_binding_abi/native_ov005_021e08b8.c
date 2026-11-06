typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef struct {
    u8 prefix[0x5E];
    u8 limit;
    u8 padding[9];
    const u8 *text;
} MessageRow;
typedef struct {
    const u16 *stream;
    u8 *target;
} BindingContext;
extern void **native_fn_02049ad0(u32 slot);
extern u16 *native_fn_02049f24(void);
extern BindingContext *native_fn_02049ae4(void);
extern u32 native_fn_02046af4(u8 *output, const u8 *text, u32 limit, u32 zero, u16 *buffer, u32 mode);
extern u16 *native_fn_02049f14(u16 *buffer);
extern u8 *native_fn_020853c8(u8 *target, const u16 *stream);
__declspec(align(4)) extern u8 native_data_021c9698[];
extern u32 native_fn_ov005_021e0a90(void);
u32 native_ov005_021e08b8(void) {
    u16 *published;
    BindingContext *context;
    u16 *buffer;
    MessageRow *row;
    const u16 *stream;
    row = *(MessageRow **)((u8 *) *native_fn_02049ad0((u32) (s8) (native_fn_ov005_021e0a90() + 5)) + 4);
    buffer = native_fn_02049f24();
    context = native_fn_02049ae4();
    native_fn_02046af4(native_data_021c9698, row->text, row->limit, 0, buffer, 0xFF);
    published = native_fn_02049f14(buffer);
    stream = context->stream;
    if (stream == (void *)0) {
        return (u32) published;
    }
    return (u32) native_fn_020853c8(context->target, stream);
}
