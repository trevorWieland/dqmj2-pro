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
extern u32 native_fn_02002e5c();
extern u32 native_fn_02003af4();
extern u32 native_fn_02003b08();
u32 native_ov001_021fbec4(void) {
    u32 temp_r0;

    native_fn_02003b08();
    native_fn_02003af4();
    native_fn_02002e5c(0x60);
    M2C_FIELD((void *)0x0400000A, u16 *, 0) = (u16) ((M2C_FIELD((void *)0x0400000A, u16 *, 0) & 0x43) | 0xD00);
    M2C_FIELD((void *)0x0400000A, u16 *, 2) = (u16) ((M2C_FIELD((void *)0x0400000A, u16 *, 2) & 0x43) | 0xE00);
    M2C_FIELD((void *)0x0400000A, u16 *, 4) = (u16) ((M2C_FIELD((void *)0x0400000A, u16 *, 4) & 0x43) | 0xF00);
    temp_r0 = (*(u32 *)0x04000000 & ~0x1F00) | 0xF00;
    *(u32 *)0x04000000 = temp_r0;
    return temp_r0;
}
