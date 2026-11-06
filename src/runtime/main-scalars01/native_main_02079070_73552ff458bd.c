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
extern u32 native_fn_02008d78();
extern u32 native_fn_02061260();
extern u32 native_fn_020620b4();
extern u32 native_fn_02079170();
extern u32 native_fn_0207a014();
extern u32 native_fn_0207a080();
extern u32 native_fn_0207df2c();
extern u32 native_fn_0207e4ac();
extern u32 native_fn_020c225c();
extern u32 native_fn_ov000_02215a14();
extern u8 native_data_020de468[];
extern u8 native_data_021c6544[];
extern u8 native_data_021c6554[];
extern u8 native_data_021c6560[];
extern u8 native_data_021c65a8[];
extern u8 native_data_021c6638[];
u32 native_main_02079070(void) {
    native_fn_02008d78(native_data_021c6638, 0, 0xF0);
    native_fn_02008d78(native_data_021c6560, 0, 0x48);
    native_fn_02008d78(native_data_021c6554, 0, 0xC);
    native_fn_ov000_02215a14();
    native_fn_0207a080();
    native_fn_020620b4(0);
    M2C_FIELD(native_data_021c6544, s32 *, 0xC) = 0;
    *(u32 *)native_data_020de468 = 0xD;
    native_fn_0207a014();
    if (native_fn_0207e4ac() != 0) {
        goto block_2;
    }
    native_fn_020c225c(0x50000000);
block_2:
    M2C_FIELD(native_data_021c6544, s32 *, 0x18) = (s32) (u8) native_fn_0207df2c(0, native_data_021c65a8);
    M2C_FIELD(native_data_021c6544, s32 *, 4) = 0;
    native_fn_02061260(1);
    native_fn_02079170();
    return 0U;
}
