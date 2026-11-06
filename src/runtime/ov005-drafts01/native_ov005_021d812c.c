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
extern u32 native_fn_ov005_021d75f8();
extern u32 native_fn_ov005_021d7778();
extern u32 native_fn_ov005_021d7e58();
extern u32 native_fn_ov005_021d81f4();
extern u8 native_data_ov005_021e78c4[];
u32 native_ov005_021d812c(void *arg0) {
    u16 temp_r0_2;
    u32 temp_r0;
    u32 temp_r0_3;
    void *temp_r4;

    temp_r4 = M2C_FIELD(native_data_ov005_021e78c4, void **, 4);
    temp_r0_3 = native_fn_ov005_021d7778(temp_r4, arg0);
    if (temp_r0_3 == 0) {
        return temp_r0_3;
    }
    temp_r0_2 = M2C_FIELD(arg0, u16 *, 8);
    switch ((s32) temp_r0_2) {
    case 7:
        temp_r0 = M2C_FIELD(temp_r4, u32 *, 0x50F0);
        if (temp_r0 == 5) {
            return temp_r0;
        }
        return native_fn_ov005_021d81f4(arg0);
    case 26:
    case 9:
        if (M2C_FIELD(temp_r4, u32 *, 0x50F0) == 1) {
            M2C_FIELD(temp_r4, s32 *, 0x50F4) = 3;
            return 3U;
        }
        M2C_FIELD(temp_r4, s32 *, 0x50F4) = 4;
        return native_fn_ov005_021d7e58(0);
    default:
        return native_fn_ov005_021d75f8(temp_r4);
    case 6:
    case 8:
        return (u32) temp_r0_2;
    }
}
