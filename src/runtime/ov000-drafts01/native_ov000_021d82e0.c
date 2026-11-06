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
extern u32 native_fn_0205e7a8();
typedef struct {
    u8 unknown_0[0x30];
    s32 field_30;
    u32 field_34;
} Record_native_data_ov000_022300c0;
extern Record_native_data_ov000_022300c0 native_data_ov000_022300c0;
extern u8 native_data_ov000_022301b8[];
u32 native_ov000_021d82e0(void) {
    if (native_data_ov000_022300c0.field_30 == 1) {
        M2C_FIELD(M2C_FIELD(native_data_ov000_022301b8, void **, 0xA0), s32 *, 0x7C) = (s32) (M2C_FIELD(M2C_FIELD(native_data_ov000_022301b8, void **, 0xA0), s32 *, 0x7C) | 2);
    }
    if (native_data_ov000_022300c0.field_34 == 1) {
        M2C_FIELD(M2C_FIELD(native_data_ov000_022301b8, void **, 0x150), s32 *, 0x7C) = (s32) (M2C_FIELD(M2C_FIELD(native_data_ov000_022301b8, void **, 0x150), s32 *, 0x7C) | 2);
    }
    if ((native_data_ov000_022300c0.field_30 != 1) && (native_data_ov000_022300c0.field_34 != 1)) {
        return native_data_ov000_022300c0.field_34;
    }
    return native_fn_0205e7a8(-1, 0x218);
}
