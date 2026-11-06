typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed int s32;
extern s32 native_fn_02026144(s32, s32);
extern s32 native_fn_ov001_021eef98(u8 *, u32);

u32 native_ov001_021f0254(s32 initial_value, u32 action, u8 *actor) {
    s32 count;
    s32 value;

    value = initial_value;
    count = (s32) native_fn_ov001_021eef98(actor, action);
    if (count > 1) {
        value = native_fn_02026144((s32)((u32)value + (u32)count - 1U), count);
    }
    return (u32) value;
}
