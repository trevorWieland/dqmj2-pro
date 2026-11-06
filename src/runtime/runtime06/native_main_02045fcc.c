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
extern u32 native_fn_020455c8();
extern u32 native_fn_020455e8();
extern u32 native_fn_020459dc();
extern u8 native_data_020f8aec[];
void native_main_02045fcc(void) {
    u8 var_r7;

    var_r7 = 0;
    do {
        if (native_fn_020455e8(var_r7) != 0) {
            native_fn_020459dc(var_r7, native_data_020f8aec + (var_r7 << 0xB), 0, 0x800);
            native_fn_020455c8(var_r7);
        }
        var_r7 += 1;
    } while ((u32) var_r7 < 4U);
}
