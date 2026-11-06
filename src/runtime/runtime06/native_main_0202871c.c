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
extern u32 native_fn_02002730();
void native_main_0202871c(void *arg0, s16 arg1, s16 arg2, s16 arg3) {
    s16 var_r1;
    s16 var_r1_2;
    s16 var_r1_3;
    void *temp_r0;

    M2C_FIELD(arg0, s16 *, 8) = arg1;
    M2C_FIELD(arg0, s16 *, 0xA) = arg2;
    temp_r0 = arg0 + 8;
    M2C_FIELD(arg0, s16 *, 0xC) = arg3;
    native_fn_02002730(temp_r0, temp_r0);
    var_r1 = M2C_FIELD(arg0, s16 *, 8);
    if ((s32) var_r1 < -0x1000) {
        var_r1 = -0x1000;
    } else if ((s32) var_r1 > (s32) (-0x1000U >> 0x14)) {
        var_r1 = (s16) (-0x1000U >> 0x14);
    }
    M2C_FIELD(arg0, s16 *, 8) = var_r1;
    var_r1_2 = M2C_FIELD(arg0, s16 *, 0xA);
    if ((s32) var_r1_2 < -0x1000) {
        var_r1_2 = -0x1000;
    } else if ((s32) var_r1_2 > (s32) (-0x1000U >> 0x14)) {
        var_r1_2 = (s16) (-0x1000U >> 0x14);
    }
    M2C_FIELD(arg0, s16 *, 0xA) = var_r1_2;
    var_r1_3 = M2C_FIELD(arg0, s16 *, 0xC);
    if ((s32) var_r1_3 < -0x1000) {
        var_r1_3 = -0x1000;
    } else if ((s32) var_r1_3 > (s32) (-0x1000U >> 0x14)) {
        var_r1_3 = (s16) (-0x1000U >> 0x14);
    }
    M2C_FIELD(arg0, s16 *, 0xC) = var_r1_3;
}
