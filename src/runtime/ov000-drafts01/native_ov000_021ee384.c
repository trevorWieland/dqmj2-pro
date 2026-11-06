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
extern u32 native_fn_02026144();
extern u32 native_fn_02062b0c();
extern u32 native_fn_02063144();
extern u32 native_fn_02065d88();
extern u32 native_fn_ov000_021ed63c();
extern u8 native_data_ov000_02236bc4[];
u32 native_ov000_021ee384(s16 arg0) {
    s16 temp_r0;
    s16 var_r5;
    s32 temp_r4;
    u32 temp_r5;
    u32 temp_r6;
    u32 temp_r6_2;
    u8 temp_r1;

    var_r5 = arg0;
    temp_r1 = M2C_FIELD(M2C_FIELD(native_data_ov000_02236bc4, void **, 4), u8 *, 0x505);
    temp_r4 = M2C_FIELD((M2C_FIELD(native_data_ov000_02236bc4, void **, 4) + (M2C_FIELD(M2C_FIELD(native_data_ov000_02236bc4, void **, 4), s32 *, 0x10) * 4)), s32 *, 0x104);
    if ((s32) (temp_r1 + var_r5) < 0) {
        var_r5 = 0 - temp_r1;
    }
    temp_r6 = native_fn_02065d88(temp_r4);
    temp_r0 = M2C_FIELD(temp_r6, u8 *, 0x27) - native_fn_02063144(temp_r4);
    if ((s32) var_r5 > (s32) temp_r0) {
        var_r5 = temp_r0;
    }
    temp_r6_2 = native_fn_02062b0c();
    if ((s32) temp_r6_2 < (s32) (var_r5 * native_fn_ov000_021ed63c(temp_r4))) {
        temp_r5 = native_fn_02062b0c();
        var_r5 = (s16) native_fn_02026144(temp_r5, native_fn_ov000_021ed63c(temp_r4));
    }
    return (u32) var_r5;
}
