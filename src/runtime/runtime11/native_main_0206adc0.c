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
extern u32 native_fn_0205e7a8();
extern u32 native_fn_02066c3c();
extern u32 native_fn_02068bf4();
extern u32 native_fn_0206be08();
extern u32 native_fn_0206be14();
extern u32 native_fn_0206c564();
extern u8 native_data_021c48f8[];
void native_main_0206adc0(void) {
    void *temp_r0;
    u32 temp_r0_2;

    temp_r0 = (void *) native_fn_02066c3c();
    temp_r0_2 = native_fn_0206c564(M2C_FIELD(temp_r0, u8 *, 1), M2C_FIELD(temp_r0, u8 *, 2));
    if (temp_r0_2 != -1U) {
        goto block_2;
    }
    return;
block_2:
    if (native_fn_02068bf4() == 0) {
        goto block_4;
    }
    native_fn_0206be08(0, 0);
    native_fn_0206be14(1);
    goto block_5;
block_4:
    native_fn_0206be08(0, 1);
    native_fn_0206be08(1, 1);
block_5:
    M2C_FIELD(native_data_021c48f8, u8 *, 0x1C) = (u8) M2C_FIELD(temp_r0, u8 *, 1);
    M2C_FIELD(native_data_021c48f8, u8 *, 0x1D) = (u8) M2C_FIELD(temp_r0, u8 *, 2);
    M2C_FIELD(native_data_021c48f8, s8 *, 0x1E) = (s8) temp_r0_2;
    M2C_FIELD(native_data_021c48f8, s8 *, 0x1F) = -1;
    native_fn_0205e7a8(-1, 0x52);
    return;
}
