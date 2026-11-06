typedef unsigned char u8;
typedef unsigned int u32;
typedef unsigned long long u64;
typedef union { u64 value; struct { u32 low; u32 high; } words; } ByteCount;
typedef struct { u32 state[4]; ByteCount count; u8 buffer[64]; } Md5Context;
extern void native_copy(const void *, void *, u32);
extern void native_md5_compress(Md5Context *);
extern void native_fill(void *, int, u32);
extern const u8 native_md5_padding[];
void saved_md5_update(Md5Context *context, const u8 *data, u32 length) {
    u32 used = context->count.words.low & 63;
    u32 space = 64 - used;
    context->count.value += length;
    if (space > length) {
        if (length) native_copy(data, context->buffer + used, length);
        return;
    }
    native_copy(data, context->buffer + used, space);
    native_md5_compress(context);
    length -= space;
    {
        int blocks = length >> 6;
        const u8 *cursor = data + space;
        if (blocks > 0) do {
            native_copy(cursor, context->buffer, 64);
            cursor += 64;
            native_md5_compress(context);
            blocks--;
        } while (blocks > 0);
        if (length & 63) native_copy(cursor, context->buffer, length & 63);
    }
}
void saved_md5_finish(u8 *output, Md5Context *context) {
    u32 high = (u32)((context->count.value << 3) >> 32);
    u32 low = (u32)(context->count.value << 3);
    u32 used;
    u32 space;
    saved_md5_update(context, native_md5_padding, 1);
    used = (u32)(context->count.value & 63ULL);
    space = 64 - used;
    if (space < 8) {
        native_fill(context->buffer + used, 0, space);
        native_md5_compress(context);
        used = 0;
        space = 64;
    }
    if (space > 8) native_fill(context->buffer + used, 0, space - 8);
    *(u32 *)(context->buffer + 56) = low;
    *(u32 *)(context->buffer + 60) = high;
    native_md5_compress(context);
    native_copy(context, output, 16);
    native_fill(context, 0, 88);
}
