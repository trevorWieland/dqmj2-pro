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
#define NULL ((void *)0)
extern u8 native_data_021d540c[];
u32 native_main_020c5868(s32 arg0) {
    s16 temp_r2;
    s32 temp_r3;
    u32 var_r4;
    u32 var_r5;
    void *var_r6;
    u32 temp_lr;

    var_r6 = NULL;
    var_r4 = 0;
    var_r5 = 0x18;
loop_1:
    temp_lr = (u32) (var_r4 + var_r5) >> 1;
    temp_r3 = temp_lr * 0x30;
    temp_r2 = *(u16 *)(native_data_021d540c + temp_r3);
    if (arg0 == temp_r2) {
        var_r6 = native_data_021d540c + temp_r3 + 4;
    } else {
        if ((s32) temp_r2 < arg0) {
            var_r5 = temp_lr - 1;
        } else {
            var_r4 = temp_lr + 1;
        }
        if (var_r4 <= var_r5) {
            goto loop_1;
        }
    }
    return (u32) var_r6;
}
