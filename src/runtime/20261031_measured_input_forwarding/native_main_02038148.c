typedef unsigned char u8;
typedef unsigned int u32;
typedef signed int s32;
extern void native_fn_020379c4(void *node, s32 value, s32 extra);

void native_main_02038148(u8 **handle, u32 value, s32 extra) {
    if (*handle != 0 && (*handle)[0x2c] != 2) {
        native_fn_020379c4(*handle + 0x1c, (s32)(value << 8), extra);
    }
}
