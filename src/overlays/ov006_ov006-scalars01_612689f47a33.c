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
extern u32 native_fn_ov006_021e3cd8();
extern u8 native_data_ov006_02218d30[];
u32 native_ov006_021e4f64(void) {
    s32 temp_r1;

    if ((s32) *(u32 *)native_data_ov006_02218d30 > 0) {
        temp_r1 = *(u32 *)native_data_ov006_02218d30 - 1;
        *(u32 *)native_data_ov006_02218d30 = temp_r1;
        if (temp_r1 == 0) {
            *(s32 *)0x04001000 = (*(s32 *)0x04001000 & ~0x1F00) | 0x1300;
        }
    }
    return native_fn_ov006_021e3cd8();
}
