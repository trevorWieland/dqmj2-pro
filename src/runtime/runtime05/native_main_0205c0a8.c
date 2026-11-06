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
extern u32 native_fn_02063f78();
extern u32 native_fn_02064978();
extern u32 native_fn_02064b24();
extern u32 native_fn_02064c8c();
extern u32 native_fn_02064d64();
extern u32 native_fn_02065128();
extern u32 native_fn_02065170();
extern u32 native_fn_020652dc();
extern u32 native_fn_02065304();
extern u32 native_fn_0206532c();
extern u32 native_fn_0206534c();
extern u32 native_fn_020655a8();
extern u32 native_fn_020655c8();
extern u32 native_fn_020655e8();
extern u32 native_fn_02065648();
extern u32 native_fn_020656b0();
extern u8 native_data_02102dc0[];
u32 native_main_0205c0a8(void) {
    native_fn_02064978();
    native_fn_020652dc(M2C_FIELD(native_data_02102dc0, u8 *, 0x61));
    native_fn_02065304(M2C_FIELD(native_data_02102dc0, u8 *, 0x62));
    native_fn_0206532c(M2C_FIELD(native_data_02102dc0, u8 *, 0x5E));
    native_fn_0206534c(M2C_FIELD(native_data_02102dc0, s8 *, 0x65));
    native_fn_02063f78();
    native_fn_020655e8();
    native_fn_02065648(M2C_FIELD(native_data_02102dc0, u8 *, 0x66));
    native_fn_020656b0(M2C_FIELD(native_data_02102dc0, u8 *, 0x6A));
    native_fn_02064b24(-1, -1, -1);
    native_fn_02064c8c(-1, -1, -1);
    if (M2C_FIELD(native_data_02102dc0, u8 *, 0x5C) == 3) {
        native_fn_02064d64(M2C_FIELD(native_data_02102dc0, s16 *, 0x56), M2C_FIELD(native_data_02102dc0, s16 *, 0x54), M2C_FIELD(native_data_02102dc0, s16 *, 0x58));
        native_fn_02065128(M2C_FIELD(native_data_02102dc0, u8 *, 0x68), M2C_FIELD(native_data_02102dc0, u8 *, 0x67), M2C_FIELD(native_data_02102dc0, u8 *, 0x69));
    } else {
        native_fn_02064d64(M2C_FIELD(native_data_02102dc0, s16 *, 0x54), M2C_FIELD(native_data_02102dc0, s16 *, 0x56), M2C_FIELD(native_data_02102dc0, s16 *, 0x58));
        native_fn_02065128(M2C_FIELD(native_data_02102dc0, u8 *, 0x67), M2C_FIELD(native_data_02102dc0, u8 *, 0x68), M2C_FIELD(native_data_02102dc0, u8 *, 0x69));
    }
    native_fn_020655c8(M2C_FIELD(native_data_02102dc0, u8 *, 0x64));
    native_fn_02065170(-1, -1, -1);
    return native_fn_020655a8(0);
}
