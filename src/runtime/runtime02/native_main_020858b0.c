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
extern u32 native_fn_02086b24();
extern u32 native_fn_02087224();
extern u32 native_fn_02087334();
u32 native_main_020858b0(void *arg0) {
    s32 temp_r1;
    s32 temp_r1_2;
    u32 temp_r5;

    temp_r5 = native_fn_0202a634();
    native_fn_02087224(arg0);
    temp_r1 = M2C_FIELD(arg0, s32 *, 0xA0);
    M2C_FIELD(arg0, s32 *, 0xA0) = (s32) (temp_r1 + 1);
    if (temp_r1 <= 5) {
        return 1U;
    }
    if (((M2C_FIELD(arg0, s32 *, 0x18) & 0x10) == 0x10) || (M2C_FIELD(temp_r5, u16 *, 2) & 0xFF7)) {
        if (((u32) (M2C_FIELD(arg0, s32 *, 0x80) << 0x1B) >> 0x1F) == 0) {
            native_fn_02086b14(arg0, 4);
            native_fn_02086b24(arg0, 5);
        }
        temp_r1_2 = M2C_FIELD(arg0, s32 *, 0x80) & ~2;
        M2C_FIELD(arg0, s32 *, 0x80) = temp_r1_2;
        if (((u32) (temp_r1_2 << 0x1C) >> 0x1F) != 0) {
            native_fn_02087334(arg0);
            M2C_FIELD(arg0, s32 *, 0x80) = (s32) (M2C_FIELD(arg0, s32 *, 0x80) & ~8);
            native_fn_0205e7a8(-1, 0x55);
        }
    }
    return 1U;
}
