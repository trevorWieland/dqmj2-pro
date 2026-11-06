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
extern u32 native_fn_020456ac();
extern u32 native_fn_02048644();
extern u32 native_fn_02048f6c();
extern u32 native_fn_0205e7a8();
extern u32 native_fn_ov005_021da8c8();
extern u32 native_fn_ov005_021db134();
extern u32 native_fn_ov005_021dbaa4();
extern u32 native_fn_ov005_021de3dc();
extern u32 native_fn_ov005_021de63c();
extern u32 native_fn_ov005_021de7f4();
extern u32 native_fn_ov005_021dead4();
extern u8 native_data_ov005_021e9818[];
typedef struct {
    u8 unknown_0[0x7c];
    s32 field_7c;
} Record_native_data_ov005_021e9a28;
extern Record_native_data_ov005_021e9a28 native_data_ov005_021e9a28;
extern u8 native_data_ov005_021e9ab8[];
typedef struct {
    u8 unknown_0[0x7c];
    s32 field_7c;
} Record_native_data_ov005_021e9ea8;
extern Record_native_data_ov005_021e9ea8 native_data_ov005_021e9ea8;
u32 native_ov005_021de1d0(void *arg0) {
    u8 temp_r1;

    M2C_FIELD(native_data_ov005_021e9818, s32 *, 0x14) = 0;
    native_fn_ov005_021db134();
    native_data_ov005_021e9a28.field_7c = (s32) (native_data_ov005_021e9a28.field_7c & ~2);
    M2C_FIELD(native_data_ov005_021e9818, s32 *, 0x68) = 1;
    temp_r1 = M2C_FIELD(arg0, u8 *, 0xAF);
    if ((temp_r1 != 1) && (temp_r1 != 2) && (temp_r1 != 3)) {
        M2C_FIELD(native_data_ov005_021e9818, s32 *, 0x68) = 0;
        if (M2C_FIELD(native_data_ov005_021e9818, s8 *, 0x66) == 1) {
            native_fn_ov005_021de3dc(arg0);
            M2C_FIELD(native_data_ov005_021e9818, void **, 0x44) = arg0;
            native_fn_0205e7a8(-1, 0x56);
            native_fn_ov005_021dbaa4();
            M2C_FIELD(native_data_ov005_021e9818, s32 *, 0x34) = 0x20;
            M2C_FIELD(native_data_ov005_021e9818, s8 *, 4) = 4;
            M2C_FIELD(native_data_ov005_021e9818, s32 *, 0x2C) = (s32) (M2C_FIELD(native_data_ov005_021e9818, s32 *, 0x2C) + 0x20);
            native_data_ov005_021e9ea8.field_7c = (s32) (native_data_ov005_021e9ea8.field_7c & ~2);
            M2C_FIELD(native_data_ov005_021e9ab8, s32 *, 0x7C) = (s32) (M2C_FIELD(native_data_ov005_021e9ab8, s32 *, 0x7C) & ~2);
            return native_fn_020456ac(0, native_fn_02048f6c(0), 2, 4, 2, 2);
        }
        goto block_7;
    }
block_7:
    native_fn_ov005_021de3dc(arg0);
    native_data_ov005_021e9ea8.field_7c = (s32) (native_data_ov005_021e9ea8.field_7c & ~2);
    M2C_FIELD(native_data_ov005_021e9ab8, s32 *, 0x7C) = (s32) (M2C_FIELD(native_data_ov005_021e9ab8, s32 *, 0x7C) & ~2);
    if (M2C_FIELD(arg0, u8 *, 0xAF) == 2) {
        native_fn_02048644(native_data_ov005_021e9ab8, M2C_FIELD(native_data_ov005_021e9818, s32 *, 0x54), 3);
        M2C_FIELD(native_data_ov005_021e9ab8, s32 *, 0x7C) = (s32) (M2C_FIELD(native_data_ov005_021e9ab8, s32 *, 0x7C) | 2);
    }
    if (M2C_FIELD(arg0, u8 *, 0xAF) == 3) {
        native_fn_02048644(native_data_ov005_021e9ab8, M2C_FIELD(native_data_ov005_021e9818, s32 *, 0x54), 4);
        M2C_FIELD(native_data_ov005_021e9ab8, s32 *, 0x7C) = (s32) (M2C_FIELD(native_data_ov005_021e9ab8, s32 *, 0x7C) | 2);
    }
    M2C_FIELD(native_data_ov005_021e9818, void **, 0x44) = arg0;
    if (M2C_FIELD(arg0, u8 *, 0xAF) == 3) {
        native_fn_ov005_021da8c8(2);
    } else {
        native_fn_ov005_021da8c8(1);
    }
    if (M2C_FIELD(native_data_ov005_021e9818, s8 *, 0x66) == 1) {
        native_fn_ov005_021de3dc(arg0);
        return native_fn_ov005_021dead4();
    }
    M2C_FIELD(native_data_ov005_021e9818, s8 *, 0x67) = 0;
    if (M2C_FIELD(native_data_ov005_021e9818, s8 *, 0x66) != 0) {
        native_fn_ov005_021dbaa4();
        M2C_FIELD(native_data_ov005_021e9818, s8 *, 4) = 6;
        return (u32) native_data_ov005_021e9818;
    }
    native_fn_ov005_021de63c();
    return native_fn_ov005_021de7f4(M2C_FIELD(native_data_ov005_021e9818, void **, 0x44));
}
