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
extern u32 native_fn_02005520();
extern u32 native_fn_0200557c();
extern u32 native_fn_020056bc();
void native_main_0202ec6c(void *arg0, s32 arg1) {
    s32 temp_r5;
    u32 temp_r2;
    u32 temp_r4;
    u32 temp_r6;
    u32 temp_r7;

    if (arg1 != 0) {
        native_fn_02005520();
    }
    temp_r2 = M2C_FIELD(arg0, u16 *, 0xC) * 8;
    if (temp_r2 != 0) {
        native_fn_0200557c(arg0 + M2C_FIELD(arg0, s32 *, 0x14), (u32) (M2C_FIELD(arg0, s32 *, 8) << 0x10) >> 0xD, temp_r2);
        M2C_FIELD(arg0, u16 *, 0x10) = (u16) (M2C_FIELD(arg0, u16 *, 0x10) | 1);
    }
    temp_r6 = M2C_FIELD(arg0, u16 *, 0x1C) * 8;
    if (temp_r6 != 0) {
        temp_r4 = M2C_FIELD(arg0, s32 *, 0x18) << 0x10;
        temp_r7 = temp_r4 >> 0xD;
        temp_r5 = M2C_FIELD(arg0, s32 *, 0x28);
        native_fn_0200557c(arg0 + M2C_FIELD(arg0, s32 *, 0x24), temp_r7, temp_r6);
        native_fn_0200557c(arg0 + temp_r5, ((u32) (0x1FFFF & (temp_r4 >> 0xD)) >> 1) + 0x20000 + ((u32) (temp_r7 & 0x40000) >> 2), temp_r6 >> 1);
        M2C_FIELD(arg0, u16 *, 0x20) = (u16) (M2C_FIELD(arg0, u16 *, 0x20) | 1);
    }
    if (arg1 == 0) {
        return;
    }
    native_fn_020056bc();
}
