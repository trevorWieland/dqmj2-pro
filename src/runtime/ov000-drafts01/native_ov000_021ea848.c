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
extern u32 native_fn_0202a1e0();
extern u32 native_fn_02040820();
extern u32 native_fn_02042288();
extern u32 native_fn_02042dd0();
extern u32 native_fn_ov000_021ea8d4();
extern u32 native_fn_ov000_021eb030();
extern u32 native_fn_ov000_0221108c();
extern u8 native_data_ov000_02236950[];
u32 native_ov000_021ea848(void) {
    s16 temp_r0;

    temp_r0 = M2C_FIELD(M2C_FIELD(native_data_ov000_02236950, void **, 0x18), s16 *, 0x1F0);
    if (temp_r0 == 0) {
        return (u32) temp_r0;
    }
    native_fn_0202a1e0(1);
    native_fn_02042288(M2C_FIELD(native_data_ov000_02236950, void **, 0x18));
    native_fn_02042dd0(M2C_FIELD(M2C_FIELD(native_data_ov000_02236950, void **, 0x18), s16 *, 0x16A));
    native_fn_ov000_0221108c();
    native_fn_0202a1e0(2);
    native_fn_ov000_021ea8d4(M2C_FIELD(native_data_ov000_02236950, s32 *, 0x20), 1);
    native_fn_ov000_021eb030();
    M2C_FIELD(M2C_FIELD(native_data_ov000_02236950, void **, 0x18), s16 *, 0x1F0) = 0;
    M2C_FIELD(M2C_FIELD(native_data_ov000_02236950, void **, 0x18), s8 *, 0x1F4) = 0;
    return native_fn_02040820();
}
