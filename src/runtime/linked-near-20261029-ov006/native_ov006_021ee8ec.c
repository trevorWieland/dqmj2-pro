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
extern u32 native_fn_02007ff4();
extern u32 native_fn_02008008();
extern u32 native_fn_02089aa4();
extern u32 native_fn_02089ba0();
extern u32 native_fn_ov006_021ee348();
typedef struct {
    s32 field_0;
    u8 unknown_4[0x4];
    s32 field_8;
    u8 unknown_c[0xc];
    s32 field_18;
    s32 field_1c;
    s32 field_20;
    s32 field_24;
} Record_native_data_ov006_0221aa80;
extern Record_native_data_ov006_0221aa80 native_data_ov006_0221aa80;
u32 native_ov006_021ee8ec(s32 arg0, s32 arg1, s32 arg2) {
    s32 temp_r0;
    u32 temp_r4;
    s32 temp_r6;
    s32 temp_r6_2;
    s32 sp0;

    sp0 = arg2;
    temp_r4 = native_fn_02007ff4();
    temp_r0 = (arg1 + 0x53) & ~3;
    native_data_ov006_0221aa80.field_24 = arg1;
    native_data_ov006_0221aa80.field_8 = temp_r0;
    temp_r6 = (temp_r0 + 0x2F) & ~0x1F;
    native_data_ov006_0221aa80.field_0 = temp_r6;
    temp_r6_2 = (temp_r6 + 0x231F) & ~0x1F;
    native_data_ov006_0221aa80.field_20 = temp_r6_2;
    M2C_FIELD(temp_r0, s32 *, 4) = (s32) ((temp_r6_2 + 0xDF) & ~0x1F);
    M2C_FIELD(native_data_ov006_0221aa80.field_8, s32 *, 8) = (s32) ((arg1 + sp0) - M2C_FIELD(native_data_ov006_0221aa80.field_8, s32 *, 4));
    M2C_FIELD(native_data_ov006_0221aa80.field_8, s32 *, 0xC) = 0;
    M2C_FIELD(native_data_ov006_0221aa80.field_8, s32 *, 0) = 3;
    native_data_ov006_0221aa80.field_1c = arg0;
    if (native_data_ov006_0221aa80.field_18 == 0) {
        if (native_fn_02089aa4(native_data_ov006_0221aa80.field_0, 0x2300) != 0) {
            native_fn_02008008(temp_r4);
            return 0U;
        }
        native_data_ov006_0221aa80.field_18 = 1;
        goto block_4;
    }
block_4:
    if (native_data_ov006_0221aa80.field_18 == 1) {
        if (native_fn_02089ba0(native_data_ov006_0221aa80.field_8, native_fn_ov006_021ee348) != 3) {
            native_fn_02008008(temp_r4);
            return 0U;
        }
        native_data_ov006_0221aa80.field_18 = 4;
        native_fn_02008008(temp_r4);
        return 1U;
    }
    native_fn_02008008(temp_r4);
    return 0U;
}
