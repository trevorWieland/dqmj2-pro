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
extern u32 native_fn_02008e0c();
extern u32 native_fn_0202a1e0();
extern u32 native_fn_02049940();
extern u32 native_fn_0205dc70();
extern u32 native_fn_0207ea7c();
extern u32 native_fn_0207eddc();
extern u32 native_fn_0207f3e4();
extern u32 native_fn_0207f454();
extern u32 native_fn_0207f860();
extern u32 native_fn_02080340();
extern u8 native_data_021c6c14[];
extern u8 native_data_021c6c38[];
extern u8 native_data_021c6c6c[];
u32 native_main_0207e720(void *arg0) {
    u32 temp_r5;
    u32 temp_r6;
    u8 temp_r0;

    temp_r5 = native_fn_0205dc70(2, 0, M2C_FIELD(arg0, u16 *, 2));
    native_fn_02008e0c(arg0, native_data_021c6c38, 0x10);
    M2C_FIELD(native_data_021c6c14, s32 *, 0x10) = 0;
    M2C_FIELD(native_data_021c6c14, s32 *, 4) = 1;
    M2C_FIELD(native_data_021c6c14, s32 *, 8) = 0;
    M2C_FIELD(native_data_021c6c14, u8 **, 0x14) = native_data_021c6c6c;
    M2C_FIELD(native_data_021c6c14, s8 *, 1) = 0;
    temp_r6 = native_fn_0202a1e0(2U);
    native_fn_02049940(1);
    native_fn_0207f3e4();
    native_fn_02080340();
    native_fn_0207ea7c();
    native_fn_0207eddc();
    native_fn_0207f454(arg0);
    temp_r0 = M2C_FIELD(arg0, u8 *, 0);
    if (temp_r0 == 1) {
        native_fn_0207f860(temp_r5, 2);
    } else if (temp_r0 == 3) {
        native_fn_0207f860(M2C_FIELD(arg0, u32 *, 8), 8);
    }
    return native_fn_0202a1e0(temp_r6);
}
