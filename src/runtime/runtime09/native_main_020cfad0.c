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
extern u32 native_fn_02062a10();
extern u32 native_fn_0206c9b4();
extern u32 native_fn_0206ccb4();
extern u32 native_fn_0206cf44();
extern u32 native_fn_0206d9c8();
extern u32 native_fn_0206da10();
extern u32 native_fn_0207cd98();
extern u32 native_fn_020cfa78();
extern u32 native_fn_020d0a14();
extern u32 native_fn_020d0a54();
u32 native_main_020cfad0(u32 arg0) {
    s32 sp8;
    s32 sp4;
    s32 temp_r0;
    s32 var_r2;
    s32 var_r3;
    s32 var_r8;
    s32 var_r9;
    u32 temp_r0_2;
    u32 temp_r6;
    void *temp_r0_3;

    temp_r0 = (s32) native_fn_020d0a14();
    var_r8 = 0;
    var_r3 = 0;
    if (temp_r0 <= 0) {
        goto block_8;
    }
loop_2:
    var_r2 = 0;
    goto loop_4;
block_3:
    var_r2 += 1;
    var_r8 += 1;
loop_4:
    if (var_r8 >= 0x64) {
        goto block_7;
    }
    if (var_r2 >= 0xC) {
        goto block_7;
    }
    goto block_3;
block_7:
    var_r3 += 1;
    if (var_r3 < temp_r0) {
        goto loop_2;
    }
block_8:
    var_r9 = 0;
    native_fn_0206d9c8();
    goto loop_12;
block_9:
    temp_r0_2 = native_fn_0207cd98(var_r8);
    if (temp_r0_2 == 0) {
        goto block_11;
    }
    temp_r6 = native_fn_020d0a54(var_r9);
    temp_r0_3 = (void *) native_fn_02062a10(temp_r0_2);
    M2C_FIELD(temp_r6, s8 *, 6) = (s8) native_fn_0206c9b4(M2C_FIELD(temp_r0_3, s16 *, 0x18), M2C_FIELD(temp_r0_3, u8 *, 0x1A), 1, 0x20, 2);
    native_fn_0206ccb4(arg0, M2C_FIELD(temp_r6, s8 *, 6), 3, 8, 0xC);
    native_fn_020cfa78(var_r9, &sp8, &sp4);
    native_fn_0206cf44(M2C_FIELD(temp_r6, s8 *, 6), (u8) sp8, (u8) sp4);
    M2C_FIELD(temp_r6, u32 *, 0) = temp_r0_2;
    var_r9 += 1;
block_11:
    var_r8 += 1;
loop_12:
    if (var_r8 >= 0x64) {
        goto block_15;
    }
    if (var_r9 >= 0xC) {
        goto block_15;
    }
    goto block_9;
block_15:
    return native_fn_0206da10();
}
