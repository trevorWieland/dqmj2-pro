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
extern u32 native_fn_02062a50();
extern u32 native_fn_02062a88();
extern u32 native_fn_02062aa0();
extern u32 native_fn_02062ad0();
extern u32 native_fn_0206dcd0();
extern u8 native_data_ov000_022372a8[];
void native_ov000_021fdd6c(s32 arg0) {
    u32 temp_r4;
    void *temp_r5;
    s32 temp_r6;

    if (arg0 != 2) {
        return;
    }
    temp_r5 = M2C_FIELD(native_data_ov000_022372a8, void **, 0xC);
    temp_r6 = M2C_FIELD(temp_r5, s32 *, 0xC);
    temp_r4 = native_fn_02062aa0();
    if (temp_r6 < (s32) (temp_r4 + native_fn_02062ad0())) {
        if (temp_r6 < (s32) native_fn_02062aa0()) {
            native_fn_02062a50(temp_r6);
        } else {
            native_fn_02062a88(M2C_FIELD(temp_r5, s32 *, 0xC) - native_fn_02062aa0());
        }
        native_fn_0206dcd0();
        return;
    }
    native_fn_0206dcd0(0);
}
