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
extern u32 native_fn_0202a1e0(u32);
extern u32 native_fn_0202a250(void);
extern u32 native_fn_0205dbf0(u32, void *, const void *, const void *, u32);
extern u32 native_fn_0205df8c(u32);
extern u32 native_fn_0205f5f4(u32);
extern u32 native_fn_0206258c(u32);
extern u32 native_fn_020675d8(u32);
extern u32 native_fn_0207cdb8(u32);
extern u32 native_fn_020bf5c0(u32);
extern u32 native_fn_020c49e8(void);
extern u32 native_fn_020cad94(void);
extern u32 native_fn_020caedc(void);
extern u32 native_fn_ov000_021f24bc(void);
extern u8 native_data_020dc348[];
extern u8 native_data_020dc368[];
typedef struct {
    u8 unknown_0[0x1];
    u8 field_1;
    u8 unknown_2[0xe];
    s32 field_10;
    u8 unknown_14[0x8];
    s32 field_1c;
} Record_native_data_021d6384;
extern Record_native_data_021d6384 native_data_021d6384;
extern u8 native_data_021d63a0[];
u32 native_main_020c5e88(void) {
    u32 temp_r4;

    native_fn_0205f5f4(native_data_021d6384.field_10);
    if (native_data_021d6384.field_1c != 0) {
        native_fn_0205dbf0(2, native_data_021d63a0, native_data_020dc368, native_data_020dc348, 0x10);
        native_data_021d6384.field_1c = 0;
        native_fn_0205df8c(0);
    }
    native_fn_020cad94();
    native_fn_020caedc();
    native_fn_020bf5c0(native_fn_0202a250());
    native_fn_0206258c(1);
    temp_r4 = native_fn_0202a1e0(2U);
    native_fn_0207cdb8(2);
    native_fn_0202a1e0(temp_r4);
    native_fn_020675d8(2);
    native_fn_020c49e8();
    if (native_data_021d6384.field_1 != 0) {
        return (u32) native_data_021d6384.field_1;
    }
    return native_fn_ov000_021f24bc();
}
