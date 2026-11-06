typedef unsigned char u8;
typedef signed int s32;
extern u8 *native_fn_02065d88(s32);

s32 native_ov000_022178cc(s32 item)
{
    return native_fn_02065d88(item)[0x2C] != 7;
}
