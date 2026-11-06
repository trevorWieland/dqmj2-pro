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
extern u32 native_fn_020444a8();
extern u32 native_fn_0207b004();
extern u32 native_fn_ov001_021dc940();
extern u32 native_fn_ov001_02210ad0();
u32 native_ov001_021ea428(void *arg0, u32 arg1) {
    u32 temp_r0;
    u32 temp_r0_2;
    u32 temp_r0_3;

    temp_r0_3 = native_fn_0207b004(arg1, 0x2000);
    if (temp_r0_3 == 0) {
        return temp_r0_3;
    }
    if ((M2C_FIELD(arg0, u8 *, 0x31E) == 0) || (native_fn_020444a8() != 0)) {
        temp_r0_2 = native_fn_ov001_02210ad0(arg0, 4, 2);
        if (temp_r0_2 == 0) {
            return temp_r0_2;
        }
        native_fn_ov001_021dc940(arg0, 0xA);
        return native_fn_ov001_021dc940(arg0, 0xB);
    }
    temp_r0 = native_fn_ov001_02210ad0(arg0, 4, 1);
    if (temp_r0 == 0) {
        return temp_r0;
    }
    native_fn_ov001_021dc940(arg0, 0xA);
    return native_fn_ov001_021dc940(arg0, 0xB);
}
