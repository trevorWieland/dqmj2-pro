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
extern u32 native_fn_02048f8c();
extern u32 native_fn_020c4220();
extern u32 native_fn_020cba28();
extern u32 native_fn_020cc730();
extern u32 native_fn_020cc740();
extern u32 native_fn_020cc75c();
extern u32 native_fn_020ccb04();
extern u32 native_fn_020ccb3c();
extern u32 native_fn_020ccea4();
extern u32 native_fn_020cd280();
extern u32 native_fn_020cece4();
extern u32 native_fn_020cf27c();
extern u8 native_data_020dc95c[];
extern u8 native_data_020e2f50[];
u32 native_main_020ce048(void) {
    u32 temp_r0;
    u32 temp_r4;
    u32 temp_r5;
    u32 temp_r5_2;

    temp_r4 = native_fn_020cc75c();
    temp_r5 = native_fn_020cc740();
    native_fn_020cd280(temp_r5, native_fn_020cf27c(), 0x10, 1, 3, 0x1E, 2);
    temp_r5_2 = native_fn_020cc740();
    native_fn_020ccea4(temp_r5_2, native_data_020dc95c[temp_r4], (temp_r4 * 6) + (s32) native_data_020e2f50, 2, 6, 0x17, *(s32 *) native_fn_020cc740());
    native_fn_020ccb04(1);
    native_fn_020ccb3c(0);
    if (native_fn_020cc730() == 2) {
        native_fn_020c4220(2, native_fn_02048f8c(1));
        native_fn_020cece4(1);
    }
    temp_r0 = native_fn_020cc730();
    if (temp_r0 != 3) {
        return temp_r0;
    }
    return native_fn_020cba28();
}
