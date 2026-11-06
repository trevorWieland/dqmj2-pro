typedef unsigned int u32;
typedef signed int s32;
typedef unsigned char u8;
extern u32 native_fn_02022998(void *digits, s32 count);
extern u32 native_fn_02022a04(void *digits, s32 count);

void native_main_02022a54(void *digits, s32 count) {
    u32 decision;
    if (count <= 0) {
        return;
    }
    if (count >= ((u8 *)digits)[4]) {
        return;
    }
    decision = native_fn_02022998(digits, count);
    ((u8 *)digits)[4] = (u8)count;
    if ((s32)decision < 0) {
        return;
    }
    native_fn_02022a04(digits, count);
}
