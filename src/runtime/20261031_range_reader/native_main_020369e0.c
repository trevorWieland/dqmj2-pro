typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed int s32;
typedef struct {
    u16 reserved;
    u16 fallback;
    u8 opaque[16];
} Base;
typedef struct {
    Base *base;
    u32 (*next)(u32 *);
} Reader;
extern u32 native_fn_0203694c(const void *, u32);
extern u32 native_fn_02036994(const void *, u32);
u32 native_main_020369e0(Reader *reader, u32 spacing, u32 cursor, u32 *nextCursor) {
    u32 total;
    u32 (*next)(u32 *);
    u32 key;
    u32 localCursor = cursor;
    next = reader->next;
    total = 0;
    key = next(&localCursor);
    if (key) {
        do {
            u32 mapped;
            if (key == 10) break;
            mapped = native_fn_0203694c(reader, key);
            if (mapped == 65535) mapped = reader->base->fallback;
            total += spacing + ((const s8 *)native_fn_02036994(reader, mapped))[2];
            key = next(&localCursor);
        } while (key);
    }
    if (nextCursor) *nextCursor = key == 10 ? localCursor : 0;
    if ((s32)total > 0) total -= spacing;
    return total;
}
