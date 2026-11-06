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
extern u32 native_fn_0202a634();
extern u32 native_fn_0205e7a8();
extern u32 native_fn_02086b14();
extern u32 native_fn_020873d4();
u32 native_main_020863dc(void *arg0) {
    u16 temp_r1;
    u32 temp_r4;

    temp_r4 = native_fn_0202a634();
    native_fn_020873d4(arg0);
    temp_r1 = M2C_FIELD(temp_r4, u16 *, 2);
    if (temp_r1 & 1) {
        native_fn_02086b14(arg0, 0x14);
        native_fn_0205e7a8(-1, 0x52);
    } else if ((M2C_FIELD(arg0, s32 *, 0x98) == 9) && (temp_r1 & 2)) {
        M2C_FIELD(arg0, s32 *, 0x24) = 1;
        native_fn_02086b14(arg0, 0x14);
        native_fn_0205e7a8(-1, 0x53);
    }
    return 1U;
}
