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
extern u32 native_fn_02046af4();
extern u32 native_fn_020470fc();
extern u32 native_fn_02085334();
extern u32 native_fn_020853c0();
extern u8 native_data_021c9698[];
extern u8 native_data_ov000_02246044[];
extern u8 native_data_ov000_02246050[];
u32 native_ov000_0221a0f0(u32 arg0) {
    native_fn_02008d78(native_data_ov000_02246050, 0, 0x40);
    native_fn_02046af4(native_data_021c9698, arg0, M2C_FIELD(M2C_FIELD(native_data_ov000_02246044, void **, 8), u8 *, 0x5E), 0, native_data_ov000_02246050, 0xFF);
    M2C_FIELD(M2C_FIELD(native_data_ov000_02246044, void **, 8), u16 *, 0x6C) = (u16) native_fn_020470fc(native_data_ov000_02246050);
    native_fn_02085334(M2C_FIELD(native_data_ov000_02246044, void **, 8), 1, native_data_ov000_02246050);
    native_fn_020853c0(M2C_FIELD(native_data_ov000_02246044, void **, 8), 3);
    return (u32) M2C_FIELD(M2C_FIELD(native_data_ov000_02246044, void **, 8), u16 *, 0x6C);
}
