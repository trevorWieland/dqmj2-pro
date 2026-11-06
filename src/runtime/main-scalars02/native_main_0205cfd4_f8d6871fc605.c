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
extern u32 native_fn_02029834();
extern u32 native_fn_02029964();
extern u32 native_fn_020413fc();
extern u8 native_data_02102e38[];
u32 native_main_0205cfd4(void *arg0) {
    s32 temp_r4;
    u32 var_r0;
    void *temp_r1;

    var_r0 = M2C_FIELD(arg0, s8 *, 1) * 0xAC;
    temp_r4 = *(u32 *)(native_data_02102e38 + var_r0);
    if (!(temp_r4 & 2)) {
        goto block_4;
    }
    temp_r1 = M2C_FIELD(arg0, void **, 0x74);
    if ((s32) M2C_FIELD(temp_r1, s32 *, 0) < (s32) ((M2C_FIELD(M2C_FIELD(temp_r1, void **, 8), u16 *, 4) << 0xC) - 1)) {
        goto block_3;
    }
    var_r0 = 4;
    M2C_FIELD(arg0, s8 *, 0) = 4;
    goto block_4;
block_3:
    var_r0 = native_fn_020413fc(arg0 + 0x14, 0x1000, M2C_FIELD(arg0, u8 *, 4));
block_4:
    if (!(temp_r4 & 4)) {
        goto block_6;
    }
    var_r0 = native_fn_02029834(arg0 + 0x14, 0x1000, M2C_FIELD(arg0, u8 *, 4));
block_6:
    if (temp_r4 & 8) {
        goto block_8;
    }
    return var_r0;
block_8:
    return native_fn_02029964(arg0 + 0x14, 0x1000, M2C_FIELD(arg0, u8 *, 4));
}
