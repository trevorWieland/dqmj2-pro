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
#define ROTATE_RIGHT(value, amount) (((u32)(value) >> ((u32)(amount) & 31)) | ((u32)(value) << ((0U - (u32)(amount)) & 31)))
extern u32 native_fn_02048034();
extern u32 native_fn_020bf218();
extern u32 native_fn_ov005_021dd788();
extern u32 native_fn_ov005_021e026c();
extern u32 native_fn_ov005_021e0730();
extern u32 native_fn_ov005_021e0818();
extern u32 native_fn_ov005_021e0838();
extern u32 native_fn_ov005_021e0a84();
extern u32 native_fn_ov005_021e0aa0();
extern u32 native_fn_ov005_021e1048();
extern u32 native_fn_ov005_021e155c();
extern u32 native_fn_ov005_021e6d64();
void native_ov005_021e2804(void) {
    s32 var_r4;
    u32 temp_r0;

    var_r4 = 0;
    if (native_fn_ov005_021dd788() == 1) {
        goto block_2;
    }
    return;
block_2:
    native_fn_ov005_021e0838();
    if (!(M2C_FIELD((void *) native_fn_ov005_021e0a84(), u16 *, 2) & 1)) {
        goto block_9;
    }
    native_fn_02048034(native_fn_020bf218() + 0xB0, 0);
    temp_r0 = native_fn_ov005_021e0aa0();
    if (temp_r0 == 0) {
        goto block_7;
    }
    if (temp_r0 != 1) {
        goto block_6;
    }
    var_r4 = 2;
block_6:
    goto block_8;
block_7:
    var_r4 = 1;
block_8:
    native_fn_ov005_021e1048(0x52);
    goto block_11;
block_9:
    if (!(M2C_FIELD((void *) native_fn_ov005_021e0a84(), u16 *, 2) & 2)) {
        goto block_11;
    }
    var_r4 = 2;
    native_fn_ov005_021e1048(0x53);
block_11:
    if (var_r4 == 1) {
        goto block_14;
    }
    if (var_r4 == 2) {
        goto block_15;
    }
    return;
block_14:
    native_fn_ov005_021e6d64();
    native_fn_ov005_021e0818();
    native_fn_ov005_021e0730(0x13, 2, 0x1B);
    native_fn_ov005_021e155c(0xF);
    return;
block_15:
    native_fn_ov005_021e155c(0xD);
    native_fn_ov005_021e0818();
    native_fn_ov005_021e026c(3, 2, 0, 0x10, 0, 0);
    return;
}
