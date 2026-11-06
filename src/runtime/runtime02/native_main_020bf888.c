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
extern u32 native_fn_020bf7e0();
extern u32 native_fn_020c0f54();
extern u8 native_data_021d4bec[];
u32 native_main_020bf888(void *arg0) {
    u32 temp_r0;

    temp_r0 = native_fn_020c0f54(M2C_FIELD(arg0, u8 *, 0), M2C_FIELD(arg0, u8 *, 1));
    if (temp_r0 == -1U) {
        return 0U;
    }
    return native_fn_020bf7e0((M2C_FIELD(native_data_021d4bec, u8 *, 4) * 6) + temp_r0);
}
