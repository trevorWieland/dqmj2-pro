typedef unsigned char u8;
typedef unsigned int u32;
typedef signed int s32;
extern u32 native_fn_020379c4(void *node, s32 value, s32 extra);

void native_main_02038148(u8 *volatile *handle, u32 value, s32 extra) {
    if (*handle != 0) {
        u8 *object = *handle;
        if (object[0x2c] == 2) return;
        native_fn_020379c4(object + 0x1c, (s32)(value << 8), extra);
    }
}
