#define NULL ((void *)0)
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
extern u32 native_fn_02008d78();
extern u32 native_fn_020824b4();
extern u32 native_fn_02082b40();
typedef struct {
    u8 unknown_0[0xa];
    s16 field_a;
    u8 unknown_c[0x4];
    s16 field_10;
    u8 unknown_12[0x32];
    s32 field_44;
} Record_native_data_021c72a0;
extern Record_native_data_021c72a0 native_data_021c72a0;
typedef struct {
    u8 unknown_0[0x6];
    s16 field_6;
    u8 unknown_8[0x2];
    u16 field_a;
    u16 field_c;
    u16 field_e;
} Record_native_data_021c73a0;
extern Record_native_data_021c73a0 native_data_021c73a0;
extern u8 native_data_021c73aa[];
u32 native_main_02082aa8(s32 arg0, void *arg1, s16 arg2) {
    native_fn_020824b4(2);
    native_data_021c72a0.field_44 = arg0;
    native_data_021c72a0.field_a = arg2;
    native_data_021c73a0.field_6 = 1;
    native_data_021c72a0.field_10 = 0;
    if (arg1 != NULL) {
        native_data_021c73a0.field_e = (u16) M2C_FIELD(arg1, u16 *, 4);
        native_data_021c73a0.field_c = (u16) M2C_FIELD(arg1, u16 *, 2);
        native_data_021c73a0.field_a = (u16) M2C_FIELD(arg1, u16 *, 0);
    } else {
        native_fn_02008d78(native_data_021c73aa, 0xFF, 6);
    }
    if (native_fn_02082b40() != 0) {
        return 1U;
    }
    native_fn_020824b4(9);
    return 0U;
}
