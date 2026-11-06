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
extern u32 native_arm7_fn_037fb420(void);
extern u16 native_arm7_data_04808158;
extern u16 native_arm7_data_0480815c;
u32 native_arm7_main_027ea5d0(s32 arg0) {
    native_arm7_data_04808158 = arg0 | 0x6000;
    native_arm7_fn_037fb420();
    return (u32) native_arm7_data_0480815c;
}
