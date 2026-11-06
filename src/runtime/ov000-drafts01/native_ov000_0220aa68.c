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
extern u32 native_fn_0205c208();
extern u32 native_fn_020c56b4();
typedef struct {
    u8 unknown_0[0x2];
    u16 field_2;
} Record_native_data_ov000_022385b8;
extern Record_native_data_ov000_022385b8 native_data_ov000_022385b8;
u32 native_ov000_0220aa68(void *arg0) {
    if (native_fn_0205c208() != 0) {
        return 0U;
    }
    if ((M2C_FIELD((void *) native_fn_020c56b4(M2C_FIELD(arg0, s16 *, 0x276)), u8 *, 7) == 5) && ((u32) M2C_FIELD(arg0, u8 *, 0x160) < 0x1FU)) {
        return 0U;
    }
    if ((u32) native_data_ov000_022385b8.field_2 < 0x96U) {
        return 0U;
    }
    return 1U;
}
