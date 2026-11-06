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
extern u32 native_fn_ov001_022122ac();
u32 native_ov001_02212544(void *arg0) {
    s32 temp_r0;
    s32 temp_r0_2;
    s32 temp_r1;

    temp_r0 = M2C_FIELD(arg0, s32 *, 0x10);
    switch (temp_r0) {
    case 0:
        M2C_FIELD(arg0, s16 *, 0x26) = (s16) (M2C_FIELD(arg0, s16 *, 0x26) - 1);
        if ((s32) M2C_FIELD(arg0, s16 *, 0x26) <= 0) {
            M2C_FIELD(arg0, s32 *, 0x10) = 1;
        }
        break;
    case 1:
        temp_r1 = M2C_FIELD(arg0, s32 *, 0x30) + M2C_FIELD(arg0, s32 *, 0x34);
        M2C_FIELD(arg0, s32 *, 0x30) = temp_r1;
        temp_r0_2 = M2C_FIELD(arg0, s32 *, 0x2C);
        if (temp_r1 >= temp_r0_2) {
            M2C_FIELD(arg0, s32 *, 0x30) = temp_r0_2;
            M2C_FIELD(arg0, s32 *, 0x10) = 2;
        }
        native_fn_ov001_022122ac(arg0, 7, M2C_FIELD(arg0, s32 *, 0x30));
        break;
    }
    if (M2C_FIELD(arg0, u8 *, 0x23) == 0) {
        return 1U;
    }
    return 0U;
}
