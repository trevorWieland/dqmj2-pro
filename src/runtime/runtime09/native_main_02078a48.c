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
extern u32 native_fn_0202a634();
extern u32 native_fn_0205e7a8();
extern u32 native_fn_0206940c();
extern u32 native_fn_020698f4();
extern u32 native_fn_0206a06c();
extern u32 native_fn_0206a0fc();
extern u32 native_fn_0206a49c();
extern u32 native_fn_0206b324();
extern u32 native_fn_0206b35c();
extern u32 native_fn_0206bf44();
extern u32 native_fn_0206c0b0();
extern u32 native_fn_02078a1c();
extern u32 native_fn_ov000_0221570c();
extern u32 native_fn_ov000_02215bc8();
extern u32 native_fn_ov000_02217dbc();
u32 native_main_02078a48(void) {
    u16 temp_r0_2;
    u32 temp_r0;
    u32 temp_r0_3;
    u32 temp_r4;
    u32 var_r5;

    var_r5 = 0;
    temp_r4 = native_fn_0202a634();
    temp_r0 = native_fn_0206a0fc(0);
    if (temp_r0 == 0) {
        goto block_6;
    }
    if (temp_r0 != 1) {
        goto block_3;
    }
    native_fn_0206bf44();
    native_fn_ov000_02215bc8();
    native_fn_ov000_0221570c(1);
    var_r5 = 1;
    goto block_16;
block_3:
    if (temp_r0 != 2) {
        goto block_5;
    }
    var_r5 = 1;
block_5:
    goto block_16;
block_6:
    if (native_fn_0206c0b0() != 0) {
        goto block_16;
    }
    native_fn_0206940c();
    temp_r0_2 = M2C_FIELD(temp_r4, u16 *, 2);
    if (!(temp_r0_2 & 1)) {
        goto block_13;
    }
    temp_r0_3 = native_fn_020698f4(0);
    if (temp_r0_3 != 1) {
        goto block_10;
    }
    native_fn_0206bf44();
    native_fn_ov000_02215bc8();
    native_fn_ov000_0221570c(1);
    var_r5 = 1;
    goto block_16;
block_10:
    if (temp_r0_3 != 2) {
        goto block_12;
    }
    var_r5 = 1;
block_12:
    goto block_16;
block_13:
    if (!(temp_r0_2 & 2)) {
        goto block_16;
    }
    if (native_fn_0206a06c(1) == 0) {
        goto block_16;
    }
    var_r5 = 1;
block_16:
    if (native_fn_0206a49c() != 2) {
        goto block_18;
    }
    native_fn_0205e7a8(-1, 0x54);
block_18:
    native_fn_0206b324(0);
    native_fn_ov000_02217dbc();
    native_fn_0206b35c();
    native_fn_02078a1c();
    return var_r5;
}
