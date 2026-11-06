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
extern u32 native_fn_02085b64();
extern u32 native_fn_02085c74();
extern u32 native_fn_02086b14();
extern u32 native_fn_02086b50();
extern u32 native_fn_02087224();
u32 native_main_02085fe4(void *arg0) {
    u32 temp_r5;

    temp_r5 = native_fn_0202a634();
    native_fn_02087224(arg0);
    if ((M2C_FIELD(arg0, u8 *, 0xAB) != 3) && (M2C_FIELD(temp_r5, u16 *, 2) & 0x30)) {
        M2C_FIELD(arg0, s32 *, 0x24) = (s32) ((M2C_FIELD(arg0, s32 *, 0x24) + 1) & 1);
        native_fn_0205e7a8(-1, 0x55);
        native_fn_02085b64(arg0);
        native_fn_02085c74(arg0);
    }
    if (M2C_FIELD(arg0, s32 *, 0x14) == 0xC) {
        native_fn_02086b14(arg0, (u8) native_fn_02086b50(arg0));
    }
    return 1U;
}
