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
extern u32 native_fn_02061c1c();
extern u32 native_fn_020624c0();
extern u32 native_fn_ov000_02223d40();
void native_ov000_021f5308(void) {
    s8 var_r9;
    u8 var_r10;

    var_r9 = 0;
    var_r10 = 8;
    do {
        if (native_fn_ov000_02223d40(native_fn_020624c0(0x13), var_r9) != 0) {
            native_fn_02061c1c((s8) (var_r9 + 6), 7, var_r10, 0xB, 2, 0, 0);
            native_fn_02061c1c((s8) (var_r9 + 9), 7, (u8) (var_r10 + 2), 0x16, 2, 1, 0);
            var_r10 += 5;
        }
        var_r9 += 1;
    } while ((s32) var_r9 < 3);
}
