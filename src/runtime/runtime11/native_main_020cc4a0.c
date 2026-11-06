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
extern u32 native_fn_020414c8();
extern u32 native_fn_02048f1c();
extern u32 native_fn_02048f2c();
extern u32 native_fn_02048f3c();
extern u32 native_fn_02048f4c();
extern u32 native_fn_02049ad0();
extern u32 native_fn_0205fd80();
extern u32 native_fn_020ccca8();
void native_main_020cc4a0(void) {
    s8 var_r8;
    void *temp_r0;

    native_fn_0205fd80(1);
    var_r8 = 0;
loop_1:
    temp_r0 = (void *) native_fn_02049ad0(var_r8);
    M2C_FIELD(temp_r0, s8 *, 4) = 5;
    M2C_FIELD(temp_r0, s8 *, 5) = 0x7F;
    M2C_FIELD(temp_r0, s32 *, 0) = 0;
    var_r8 += 1;
    M2C_FIELD(temp_r0, s8 *, 6) = -1;
    if ((s32) var_r8 < 0x24) {
        goto loop_1;
    }
    native_fn_020ccca8();
    native_fn_020414c8(0x3F);
    native_fn_02048f3c(0, 1);
    native_fn_02048f2c(2, 1);
    native_fn_02048f1c(1, 1);
    native_fn_02048f4c(3, 1);
    M2C_FIELD((void *)0x04001008, u16 *, 0) = (u16) (M2C_FIELD((void *)0x04001008, u16 *, 0) & ~3);
    M2C_FIELD((void *)0x04001008, u16 *, 4) = (u16) ((M2C_FIELD((void *)0x04001008, u16 *, 4) & ~3) | 1);
    M2C_FIELD((void *)0x04001008, u16 *, 2) = (u16) ((M2C_FIELD((void *)0x04001008, u16 *, 2) & ~3) | 2);
    M2C_FIELD((void *)0x04001008, u16 *, 6) = (u16) ((M2C_FIELD((void *)0x04001008, u16 *, 6) & ~3) | 3);
    return;
}
