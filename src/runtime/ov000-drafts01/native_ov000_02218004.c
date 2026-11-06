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
extern u32 native_fn_02008c58();
extern u32 native_fn_020414c8();
extern u32 native_fn_020418b0();
extern u32 native_fn_02045738();
extern u32 native_fn_02048e74();
extern u32 native_fn_ov000_02218b4c();
typedef struct {
    u8 unknown_0[0xc];
    u32 field_c;
    u8 unknown_10[0x4c];
    s32 field_5c;
} Record_native_data_ov000_02245e54;
extern Record_native_data_ov000_02245e54 native_data_ov000_02245e54;
extern u8 native_data_ov000_02245eac[];
u32 native_ov000_02218004(void) {
    native_fn_02048e74(native_data_ov000_02245eac, 0);
    native_data_ov000_02245e54.field_5c = 0;
    native_fn_ov000_02218b4c();
    M2C_FIELD((void *)0x04001008, u16 *, 0) = (u16) ((M2C_FIELD((void *)0x04001008, u16 *, 0) & 0x43) | 0xC1C);
    M2C_FIELD((void *)0x04001008, u16 *, 2) = (u16) ((M2C_FIELD((void *)0x04001008, u16 *, 2) & 0x43) | 0xC010);
    M2C_FIELD((void *)0x04001008, u16 *, 4) = (u16) ((M2C_FIELD((void *)0x04001008, u16 *, 4) & 0x43) | 0xC410);
    M2C_FIELD((void *)0x04001008, u16 *, 6) = (u16) ((M2C_FIELD((void *)0x04001008, u16 *, 6) & 0x43) | 0xC808);
    M2C_FIELD((void *)0x04001008, u16 *, 0) = (u16) (M2C_FIELD((void *)0x04001008, u16 *, 0) & ~3);
    M2C_FIELD((void *)0x04001008, u16 *, 2) = (u16) ((M2C_FIELD((void *)0x04001008, u16 *, 2) & ~3) | 1);
    M2C_FIELD((void *)0x04001008, u16 *, 4) = (u16) ((M2C_FIELD((void *)0x04001008, u16 *, 4) & ~3) | 2);
    M2C_FIELD((void *)0x04001008, u16 *, 6) = (u16) ((M2C_FIELD((void *)0x04001008, u16 *, 6) & ~3) | 3);
    native_fn_02008c58(0, 0x06200000, 0x20000);
    *(s32 *)0x04001000 = (*(s32 *)0x04001000 & ~0x1F00) | 0x1F00;
    if (native_data_ov000_02245e54.field_c == 0) {
        return native_data_ov000_02245e54.field_c;
    }
    native_fn_02008c58(0, 0x06600000, 0x20000);
    native_fn_02008c58(0, 0x05000400, 0x400);
    native_fn_02045738(1);
    native_fn_020414c8(0x3F);
    return native_fn_020418b0(2);
}
