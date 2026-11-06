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
extern u32 native_fn_0202a1e0();
extern u32 native_fn_02048e74();
extern u32 native_fn_02048fcc();
extern u32 native_fn_02068ae8();
extern u32 native_fn_0206c484();
extern u32 native_fn_020cc730();
extern u32 native_fn_020cc740();
extern u32 native_fn_020cc75c();
extern u32 native_fn_020cde08();
extern u8 native_data_021d6964[];
extern u8 native_data_021d696c[];
u32 native_main_020cd788(void) {
    u32 temp_r4;
    void *temp_r0;

    native_fn_02048e74(native_data_021d696c, 2);
    native_fn_020cc740();
    native_fn_02048fcc();
    if (native_fn_020cc75c() == 2) {
        native_fn_0206c484(1);
    }
    temp_r4 = native_fn_0202a1e0(2U);
    native_fn_02068ae8();
    native_fn_0202a1e0(temp_r4);
    if (native_fn_020cc730() == 1) {
        M2C_FIELD(native_data_021d6964, s32 *, 4) = 1;
        native_fn_020cde08();
    } else if (native_fn_020cc730() == 0) {
        M2C_FIELD(native_data_021d6964, s32 *, 4) = 0;
        native_fn_020cde08();
    }
    M2C_FIELD(native_data_021d6964, s32 *, 0) = 1;
    M2C_FIELD(native_data_021d6964, s32 *, 0xC) = 0;
    *(s32 *) native_fn_020cc740() = 0xF;
    temp_r0 = (void *) native_fn_020cc740();
    M2C_FIELD(temp_r0, s8 *, 0x10) = 2;
    return (u32) temp_r0;
}
