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
extern u32 native_fn_0201b248();
extern u32 native_fn_020b3b50();
extern u32 native_fn_020b3b80();
extern u32 native_fn_020b3bb8();
extern u32 native_fn_020b4108();
extern u8 native_data_020e1714[];
u32 native_main_020b56e8(void *arg0, u8 *arg1, s32 arg2) {
    s32 temp_r2;
    s32 temp_r7;
    s32 sp4;
    s32 sp0;

    if ((arg2 < 2) || (native_fn_0201b248(arg1 + M2C_FIELD(M2C_FIELD(arg0, void **, 8), s32 *, 0x44), native_data_020e1714, 2) != 0)) {
        if (native_fn_020b4108(arg0, arg1, arg2) == 0) {
            return 0U;
        }
        return 1U;
    }
    temp_r7 = arg2 + 2;
    if ((s32) native_fn_020b3b50(arg0 + 0x50) < temp_r7) {
        return 1U;
    }
    sp0 = M2C_FIELD(arg0, s32 *, 0x50);
    sp4 = M2C_FIELD(arg0, s32 *, 0x58);
    if (M2C_FIELD(M2C_FIELD(arg0, void **, 8), s32 *, 0x40) == 2) {
        native_fn_020b3b80(arg0 + 0x50, arg1, 2);
    }
    native_fn_020b3b80(arg0 + 0x50, native_data_020e1714, 2);
    temp_r2 = M2C_FIELD(M2C_FIELD(arg0, void **, 8), s32 *, 0x44);
    native_fn_020b3b80(arg0 + 0x50, &arg1[temp_r2], arg2 - temp_r2);
    if (native_fn_020b4108(arg0, sp0 + sp4, temp_r7) == 0) {
        return 0U;
    }
    native_fn_020b3bb8(arg0 + 0x50, -1, temp_r7);
    return 1U;
}
