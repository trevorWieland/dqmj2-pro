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
extern u32 native_fn_0207afec();
extern u32 native_fn_ov001_021db0d8();
extern u32 native_fn_ov001_021e81d0();
extern u32 native_fn_ov001_0220d6a4();
extern u8 native_data_ov001_022388ec[];
u32 native_ov001_021df558(void) {
    native_fn_ov001_0220d6a4();
    if ((M2C_FIELD(native_data_ov001_022388ec, u8 *, 7) == 0) && (M2C_FIELD(native_data_ov001_022388ec, u8 *, 0x1B) == 0)) {
        goto block_7;
    }
    if (((M2C_FIELD(native_data_ov001_022388ec, u8 *, 7) != 0) && (M2C_FIELD(M2C_FIELD(native_data_ov001_022388ec, void **, 0x48), u8 *, 0x31E) == 0)) || ((M2C_FIELD(native_data_ov001_022388ec, u8 *, 0x1B) != 0) && (M2C_FIELD(M2C_FIELD(native_data_ov001_022388ec, void **, 0x48), u8 *, 0x31E) == 1))) {
block_7:
        if (((s32) (M2C_FIELD(native_data_ov001_022388ec, s8 *, 0x1A) + 1) >= (s32) M2C_FIELD(native_data_ov001_022388ec, s8 *, 0xA)) || (M2C_FIELD((void *) native_fn_0207afec(M2C_FIELD(native_data_ov001_022388ec, u16 *, 0x36)), s8 *, 0x26) == 1)) {
            native_fn_ov001_021db0d8(M2C_FIELD(native_data_ov001_022388ec, void **, 0x48), 1);
        } else {
            native_fn_ov001_021db0d8(M2C_FIELD(native_data_ov001_022388ec, void **, 0x48), 0);
        }
    }
    M2C_FIELD(M2C_FIELD(native_data_ov001_022388ec, void **, 0x48), u16 *, 0x344) = (u16) *(u16 *) native_fn_ov001_021e81d0(M2C_FIELD(M2C_FIELD(native_data_ov001_022388ec, void **, 0x48), u8 *, 0x31E), M2C_FIELD(M2C_FIELD(native_data_ov001_022388ec, void **, 0x48), u8 *, 0x31F));
    M2C_FIELD(native_data_ov001_022388ec, s8 *, 8) = 0x10;
    return 0U;
}
