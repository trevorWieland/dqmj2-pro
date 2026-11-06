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
extern u32 native_fn_02063734();
extern u32 native_fn_ov000_022036c4();
extern u32 native_fn_ov000_0220552c();
extern u32 native_fn_ov000_02205bec();
extern u8 native_data_ov000_02236d98[];
u32 native_ov000_021f26b4(void) {
    s32 temp_r0_2;
    s8 temp_r0;
    u32 temp_r1;

    temp_r0 = M2C_FIELD(M2C_FIELD(native_data_ov000_02236d98, void **, 8), s8 *, 0x20);
    switch (temp_r0) {
    default:
        return (u32) temp_r0;
    case 2:
        temp_r1 = M2C_FIELD((M2C_FIELD(native_data_ov000_02236d98, void **, 8) + (M2C_FIELD(M2C_FIELD(native_data_ov000_02236d98, void **, 8), s32 *, 0x10) * 4)), u32 *, 0x10C);
        return native_fn_ov000_022036c4((s16) temp_r1, temp_r1 >> 0x10);
    case 4:
        temp_r0_2 = M2C_FIELD((M2C_FIELD(native_data_ov000_02236d98, void **, 8) + (M2C_FIELD(M2C_FIELD(native_data_ov000_02236d98, void **, 8), s32 *, 0x10) * 4)), s32 *, 0x10C);
        return native_fn_ov000_0220552c((u8) temp_r0_2, (u8) native_fn_02063734((u8) temp_r0_2), 0, 1);
    case 6:
        return native_fn_ov000_02205bec((u8) M2C_FIELD((M2C_FIELD(native_data_ov000_02236d98, void **, 8) + (M2C_FIELD(M2C_FIELD(native_data_ov000_02236d98, void **, 8), s32 *, 0x10) * 4)), s32 *, 0x10C));
    }
}
