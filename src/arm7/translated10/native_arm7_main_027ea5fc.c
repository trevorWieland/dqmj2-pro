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
extern u32 native_arm7_data_0480815a;
u32 native_arm7_main_027ea5fc(s32 arg0, s16 arg1) {
    M2C_FIELD((u32) &native_arm7_data_0480815a, s16 *, 0) = arg1;
    M2C_FIELD((u32) &native_arm7_data_0480815a, s16 *, -2) = (s16) (arg0 | 0x5000);
    if (native_arm7_fn_037fb420() != 0) {
        return -1U;
    }
    return 0U;
}
