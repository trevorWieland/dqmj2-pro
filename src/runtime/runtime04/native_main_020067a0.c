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
extern u32 native_fn_020062a4();
extern u32 native_fn_02006388();
extern u32 native_fn_02006924();
extern u32 native_fn_020069dc();
extern u32 native_fn_02006c70();
extern u32 native_fn_02006ca4();
extern u32 native_fn_0200716c();
extern u32 native_fn_02008430();
extern u8 native_data_020e33c0[];
void native_main_020067a0(void) {
    s32 temp_r0;
    void *temp_r4;

    temp_r4 = *M2C_FIELD(native_data_020e33c0, void ***, 8);
    native_fn_02006c70();
    native_fn_0200716c(temp_r4);
    temp_r0 = M2C_FIELD(temp_r4, s32 *, 0x78);
    if (temp_r0 != 0) {
        native_fn_020062a4(temp_r0, temp_r4);
    }
    native_fn_02006388(temp_r4);
    M2C_FIELD(temp_r4, s32 *, 0x64) = 2;
    native_fn_02006924(temp_r4 + 0x9C);
    native_fn_02006ca4();
    native_fn_020069dc();
    native_fn_02008430();
}
