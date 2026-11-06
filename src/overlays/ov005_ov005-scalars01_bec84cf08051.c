typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
typedef float f32;
typedef double f64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
#define MULT_HI(a, b) ((s32)(((s64)(s32)(a) * (s32)(b)) >> 32))
#define MULTU_HI(a, b) ((u32)(((u64)(u32)(a) * (u32)(b)) >> 32))
#define ROTATE_RIGHT(value, amount) (((u32)(value) >> ((u32)(amount) & 31)) | ((u32)(value) << ((0U - (u32)(amount)) & 31)))
extern u32 native_fn_02007ff4();
extern u32 native_fn_02008008();
extern u32 native_fn_02008430();
extern u32 native_fn_ov005_021d738c();
extern u32 native_fn_ov005_021d7404();
extern u32 native_fn_ov005_021d75c4();
extern u32 native_fn_ov005_021d75e0();
extern u8 native_data_ov005_021e78cc[];
u32 native_ov005_021d9158(u32 arg0, u32 arg1, u32 arg2, u32 arg3, s32 arg4, s32 arg5, s32 arg6) {
    u32 temp_r0;
    u32 temp_r0_2;
    u32 temp_r4;

    temp_r4 = native_fn_02007ff4();
    if (native_fn_ov005_021d7404(*(u32 *)native_data_ov005_021e78cc + 0x5760, 0, arg0, 1) == 0) {
        temp_r0 = native_fn_ov005_021d7404(*(u32 *)native_data_ov005_021e78cc + 0x5760, 0, 0, 1);
        if (temp_r0 == 0) {
            native_fn_02008430();
        } else {
            temp_r0_2 = native_fn_ov005_021d738c(arg6);
            if (temp_r0_2 == 0) {
                native_fn_02008430();
            }
            native_fn_ov005_021d75c4(temp_r0, arg0, arg1, temp_r0_2);
            native_fn_ov005_021d75e0(temp_r0, arg2, arg3, arg4, arg5);
        }
    }
    return native_fn_02008008(temp_r4);
}
