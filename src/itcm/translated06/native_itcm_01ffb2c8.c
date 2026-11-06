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
extern u32 native_fn_01ffae70();
extern u32 native_fn_01ffb0bc();
extern u32 native_fn_01ffb324();
extern u32 native_fn_01ffb368();
extern u32 native_data_01fff950;
u32 native_itcm_01ffb2c8(s32 arg0, s32 arg1, s32 arg2, s32 arg3, s32 arg4) {
    native_fn_01ffae70(arg0, arg1, arg2, 0x57, arg4);
    if (arg3 != 0) {
        native_fn_01ffb0bc((s8) (native_fn_01ffb368() + 5));
    }
    native_data_01fff950 = 1;
    native_fn_01ffb324(0);
    return 1U;
}
