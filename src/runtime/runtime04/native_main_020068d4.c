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
extern u32 native_fn_020061f8();
extern u32 native_fn_020063d0();
extern u32 native_fn_02007ff4();
extern u32 native_fn_02008008();
extern u8 native_data_020e33c0[];
void native_main_020068d4(s32 arg0) {
    u32 temp_r4;
    void *temp_r5;

    temp_r4 = native_fn_02007ff4();
    temp_r5 = *M2C_FIELD(native_data_020e33c0, void ***, 8);
    if (arg0 != 0) {
        M2C_FIELD(temp_r5, s32 *, 0x78) = arg0;
        native_fn_020061f8(arg0, temp_r5);
    }
    M2C_FIELD(temp_r5, s32 *, 0x64) = 0;
    native_fn_020063d0();
    native_fn_02008008(temp_r4);
}
