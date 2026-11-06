typedef unsigned char u8;
typedef signed int s32;
extern u8 *native_fn_02065d88(s32 item);
extern s32 native_fn_0203d294(s32 bound);

s32 native_main_02065dec(s32 item)
{
    u8 *descriptor = native_fn_02065d88(item);
    return descriptor[0x25] > native_fn_0203d294(100);
}
