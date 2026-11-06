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
extern u32 native_fn_0201b248();
extern u32 native_fn_0207e714();
extern u32 native_fn_0207f3b0();
extern u8 native_data_020de57c[];
extern u8 native_data_021c6d80[];
extern u8 native_data_021c6d88[];
u32 native_main_0207fb3c(void) {
    u8 temp_r0;
    s32 var_r1;
    s32 var_r6;
    u8 *var_r7;
    u8 *var_r8;
    u32 temp_r9;
    u8 *var_r10;

    var_r8 = native_data_021c6d88;
    temp_r9 = native_fn_0207e714();
    var_r7 = native_fn_0207f3b0();
    var_r6 = 0;
    if ((s32) *native_data_021c6d80 > 0) {
        var_r10 = native_data_021c6d88;
loop_2:
        if ((native_fn_0201b248(var_r10, temp_r9, 3) != 0) && (*var_r10 != 0)) {
            var_r1 = 0;
            do {
                temp_r0 = var_r8[var_r1];
                var_r1 += 1;
                *var_r7 = temp_r0;
                var_r7 += 1;
            } while (var_r10[var_r1] != 0);
            var_r6 += 1;
            var_r8 += 3;
            var_r10 += 3;
            if (var_r6 < (s32) *native_data_021c6d80) {
                goto loop_2;
            }
        }
    }
    *var_r7 = 0;
    *native_data_020de57c = 1;
    return (u32) native_data_020de57c;
}
