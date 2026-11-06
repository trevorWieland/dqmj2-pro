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
extern u32 native_fn_0205e73c();
extern u32 native_fn_0205e7a8();
extern u32 native_fn_0205e7f4();
extern u32 native_fn_0205e814();
extern u32 native_fn_0205f2d8();
extern u32 native_fn_0205f5dc();
extern u32 native_fn_0205f5f4();
typedef struct { u8 unknown[0x1C]; u32 word1C; s32 word20; u8 state24; u8 counter25; u8 handle26; } ObservedState;
extern ObservedState native_data_021079a0;
extern u8 native_data_021079bc[];
u32 native_main_0205e938(void) {
    u8 temp_r2;
    u8 temp_r2_2;
    u8 temp_r2_3;
    u32 var_r4;
    s32 var_r6;
    u8 *var_r7;
    u8 *var_r7_2;
    s32 var_r8;

    var_r4 = 0;
    if (native_data_021079a0.state24 != 0xA) {
        goto block_7;
    }
    if (++native_data_021079a0.counter25 <= 0x12U) {
        goto block_24;
    }
    var_r7 = native_data_021079bc;
    var_r6 = 0;
loop_3:
    if ((s32) M2C_FIELD(var_r7, s8 *, 0xB) < 0) {
        goto block_5;
    }
    native_fn_0205e7f4(var_r6, 1);
block_5:
    var_r6 += 1;
    var_r7 += 1;
    if (var_r6 < 0x10) {
        goto loop_3;
    }
    native_data_021079a0.word1C = native_fn_0205f5dc();
    native_fn_0205e73c(native_data_021079a0.word20);
    native_data_021079a0.counter25 = 0U;
    native_data_021079a0.state24 = 0x14U;
    goto block_24;
block_7:
    if (native_data_021079a0.state24 != 0x14) {
        goto block_10;
    }
    if (++native_data_021079a0.counter25 <= 6U) {
        goto block_24;
    }
    native_data_021079a0.handle26 = (u8) native_fn_0205e7a8(-1, native_data_021079a0.word20);
    native_data_021079a0.state24 = 0x1EU;
    goto block_24;
block_10:
    if (native_data_021079a0.state24 != 0x1E) {
        goto block_13;
    }
    if (native_fn_0205f2d8(native_data_021079a0.handle26) != 0) {
        goto block_24;
    }
    native_fn_0205f5f4(native_data_021079a0.word1C);
    native_data_021079a0.counter25 = 0U;
    native_data_021079a0.state24 = 0x28U;
    goto block_24;
block_13:
    if (native_data_021079a0.state24 != 0x28) {
        goto block_20;
    }
    if (++native_data_021079a0.counter25 <= 0xFU) {
        goto block_24;
    }
    var_r7_2 = native_data_021079bc;
    var_r8 = 0;
loop_16:
    if ((s32) M2C_FIELD(var_r7_2, s8 *, 0xB) < 0) {
        goto block_18;
    }
    native_fn_0205e7f4(var_r8, 0);
    native_fn_0205e814(var_r8, M2C_FIELD(var_r7_2, s8 *, 0xB), 0xF);
block_18:
    var_r8 += 1;
    var_r7_2 += 1;
    if (var_r8 < 0x10) {
        goto loop_16;
    }
    native_data_021079a0.state24 = 0x32U;
    goto block_24;
block_20:
    if (native_data_021079a0.state24 != 0x32) {
        goto block_22;
    }
    native_data_021079a0.state24 = 0U;
    var_r4 = 1;
    goto block_24;
block_22:
    if (native_data_021079a0.state24 != 0) {
        goto block_24;
    }
    var_r4 = 1;
block_24:
    return var_r4;
}
