typedef signed char s8;
typedef unsigned char u8;
typedef int s32;
extern u8 *native_fn_01ffb4ec(u8);

s32 native_itcm_01ffa8f0(s32 value) {
    s8 index;
    for (index = 0; index < 8; index++) {
        if (*(s8 *)(native_fn_01ffb4ec((u8)index) + 0x165) == value) {
            return *(s8 *)(native_fn_01ffb4ec((u8)index) + 0x16e);
        }
    }
    return 0;
}
