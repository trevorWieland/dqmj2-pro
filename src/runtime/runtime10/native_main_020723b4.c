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
extern u32 native_fn_02049f4c();
extern u32 native_fn_02061944();
extern u32 native_fn_02061dcc();
extern u32 native_fn_02062144();
extern u32 native_fn_02062328();
extern u32 native_fn_0206de44();
extern u32 native_fn_02072490();
extern u32 native_fn_020724f4();
extern u8 native_data_021c4f60[];
u32 native_main_020723b4(void) {
    s8 temp_r0_2;
    void *temp_r0;
    u32 var_r5;
    s8 var_r6;
    s8 temp_r7;

    temp_r0 = (void *) native_fn_02061944();
    temp_r0_2 = M2C_FIELD(temp_r0, s8 *, 0x26A);
    var_r5 = 0;
    switch (temp_r0_2) {
    case 0:
        native_fn_02072490();
        M2C_FIELD(temp_r0, s8 *, 0x26A) = 1;
        native_fn_0206de44();
        
    case 1:
        if (M2C_FIELD(native_data_021c4f60, s8 *, 0x2C) != 0) {
            native_fn_02062328();
            native_fn_02062144(M2C_FIELD(temp_r0, s8 *, 0x26F), 0);
            var_r6 = 0;
            do {
                temp_r7 = var_r6 + 6;
                native_fn_02061dcc(temp_r7);
                native_fn_02049f4c();
                native_fn_020724f4(temp_r7, var_r6);
                var_r6 += 1;
            } while ((s32) var_r6 < 2);
            native_fn_0206de44(0);
        }
        break;
    }
    if (M2C_FIELD(temp_r0, s8 *, 0x26C) != 0x2A) {
        var_r5 = 1;
    }
    return var_r5;
}
