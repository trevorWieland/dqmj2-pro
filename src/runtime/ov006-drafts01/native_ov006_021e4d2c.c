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
extern u32 native_fn_020bb1b4();
extern u32 ov006_noop_021e3cd4();
extern u8 native_data_ov006_02218d2c[];
extern u8 native_data_ov006_02218d30[];
extern u8 native_data_ov006_02218d34[];
extern u8 native_data_ov006_02218d38[];
extern u8 native_data_ov006_02218d54[];
u32 native_ov006_021e4d2c(void) {
    ov006_noop_021e3cd4();
    M2C_FIELD(native_data_ov006_02218d30, u8 **, 8) = native_data_ov006_02218d54;
    *native_data_ov006_02218d2c = 0;
    return native_fn_020bb1b4(1, native_data_ov006_02218d38, native_data_ov006_02218d2c, native_data_ov006_02218d34);
}
