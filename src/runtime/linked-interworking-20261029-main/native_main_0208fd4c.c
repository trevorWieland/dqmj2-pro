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
extern u32 native_fn_02006890();
extern u32 native_fn_02007ff4();
extern u32 native_fn_02008008();
extern u32 native_fn_0208d754();
extern u32 native_fn_0208d7e0();
extern u32 native_fn_0208d8e8();
extern u32 native_fn_0208d910();
extern u32 native_fn_0208ec1c();
extern u32 native_fn_02090238();
extern u32 native_fn_02090248();
u32 native_main_0208fd4c(void *arg0) {
    s32 var_r0;
    s8 temp_r0;
    s32 var_r1;
    void *temp_r4;
    u32 temp_r5;

    temp_r4 = M2C_FIELD(arg0, void **, 4);
    temp_r0 = M2C_FIELD(temp_r4, s8 *, 0x73);
    var_r1 = 1;
    if ((temp_r0 != 0) && (temp_r0 != 4)) {
        var_r1 = 0;
    }
    if (var_r1 != 0) {
        native_fn_02006890(M2C_FIELD(temp_r4, s32 *, 0x68) + 0x20);
        native_fn_0208d8e8();
        native_fn_0208d910();
        native_fn_0208d7e0();
    }
    native_fn_0208d754();
    M2C_FIELD(temp_r4, s16 *, 0x70) = (s16) (M2C_FIELD(temp_r4, s16 *, 0x70) & ~6);
    if (M2C_FIELD(temp_r4, s8 *, 0x73) == 2) {
        var_r0 = M2C_FIELD(temp_r4, s32 *, 0x68);
    } else {
        var_r0 = M2C_FIELD(temp_r4, s32 *, 0x64);
    }
    native_fn_0208ec1c(var_r0, 0);
    temp_r5 = native_fn_02007ff4();
    native_fn_02090248(temp_r4);
    native_fn_02090238(temp_r4);
    native_fn_02008008(temp_r5);
    M2C_FIELD(temp_r4, s16 *, 0x70) = (s16) (0x20 | M2C_FIELD(temp_r4, s16 *, 0x70));
    return 0U;
}
