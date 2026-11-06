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
extern u32 native_fn_020bef78();
extern u32 native_fn_020bf218();
extern u32 native_fn_ov005_021e0708();
extern u32 native_fn_ov005_021e0818();
extern u32 native_fn_ov005_021e0a84();
extern u32 native_fn_ov005_021e1048();
extern u32 native_fn_ov005_021e155c();
typedef struct {
    u8 unknown_0[0x64];
    s32 field_64;
} Record_native_data_ov005_021ed438;
extern Record_native_data_ov005_021ed438 native_data_ov005_021ed438;
void native_ov005_021e3234(void) {
    u32 temp_r0;

    if (M2C_FIELD((void *) native_fn_ov005_021e0a84(), u16 *, 2) & 0xFF7) {
        goto block_2;
    }
    return;
block_2:
    native_fn_ov005_021e0818();
    native_fn_ov005_021e1048(0x52);
    temp_r0 = native_fn_020bef78();
    if (temp_r0 == 0) {
        goto block_6;
    }
    if (temp_r0 == 1) {
        goto block_6;
    }
    if (temp_r0 == 2) {
        goto block_6;
    }
    goto block_7;
block_6:
    native_fn_02048034(native_fn_020bf218() + 0xB0, 0);
    native_fn_ov005_021e0708(0x13, 2, 0xE);
    native_fn_ov005_021e155c(0x35);
    native_data_ov005_021ed438.field_64 = 0x3C;
    return;
block_7:
    native_fn_ov005_021e155c(0x1C);
    return;
}
