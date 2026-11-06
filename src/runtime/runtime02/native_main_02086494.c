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
extern u32 native_fn_02046384();
extern u32 native_fn_02085270();
extern u32 native_fn_02086948();
extern u32 native_fn_02086b14();
extern u32 native_fn_02087674();
extern u8 native_data_021c9698[];
u32 native_main_02086494(void *arg0) {
    u8 temp_r1;
    u8 temp_r1_2;

    native_fn_02086948(arg0, 0);
    temp_r1 = M2C_FIELD(arg0, u8 *, 0x38) - ((s32) (native_fn_02087674(native_data_021c9698, arg0 + 0x3C, 0) + 7) >> 4);
    native_fn_02085270(arg0 + 0x3C, (s16) (temp_r1 * 8), M2C_FIELD(arg0, u8 *, 0x39));
    M2C_FIELD(arg0, u8 *, 0x32) = (u8) (temp_r1 - 2);
    M2C_FIELD(arg0, u8 *, 0x33) = (u8) M2C_FIELD(arg0, u8 *, 0x1D);
    M2C_FIELD(arg0, u8 *, 0x34) = 4U;
    temp_r1_2 = M2C_FIELD(arg0, u8 *, 0x1F);
    M2C_FIELD(arg0, u8 *, 0x35) = temp_r1_2;
    native_fn_02046384(M2C_FIELD(arg0, u8 *, 0x2E), M2C_FIELD(arg0, u8 *, 0x32), M2C_FIELD(arg0, u8 *, 0x33), M2C_FIELD(arg0, u8 *, 0x34), (s32) temp_r1_2, 0, (s32) M2C_FIELD(arg0, u8 *, 0x3A));
    native_fn_02086b14(arg0, 0x17);
    return 1U;
}
