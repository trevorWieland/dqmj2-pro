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
extern u32 native_fn_02048f8c();
extern u32 native_fn_020620e8();
extern u32 native_fn_02062378();
extern u32 native_fn_020c4220();
extern u32 native_fn_020c48e8();
extern u32 native_fn_020cba28();
extern u32 native_fn_020cba38();
extern u32 native_fn_020cc730();
extern u32 native_fn_020cc740();
extern u32 native_fn_020cc76c();
extern u32 native_fn_020ccb04();
extern u32 native_fn_020ccb3c();
extern u32 native_fn_020ccfc4();
extern u32 native_fn_020cf26c();
u32 native_main_020cbfa8(void) {
    u32 temp_r0;
    u32 temp_r4;
    u32 temp_r4_2;
    u32 temp_r5;

    temp_r5 = native_fn_020cc740();
    native_fn_020ccfc4(temp_r5, 9, 2, 4, 0x17, *(s32 *) native_fn_020cc740());
    if (native_fn_020cc730() == 2) {
        native_fn_020c4220(2, native_fn_02048f8c(1));
    }
    native_fn_020c48e8(0x57);
    native_fn_020ccb04(1);
    native_fn_020ccb3c(0);
    if ((native_fn_020cc730() != 1) && (native_fn_020cc730() != 3)) {
        native_fn_020620e8(0x20, 1);
        temp_r4_2 = native_fn_020cf26c();
        native_fn_020cba38(temp_r4_2, native_fn_020cc76c());
    }
    if (native_fn_020cc730() == 3) {
        native_fn_020cba28();
    }
    temp_r0 = native_fn_02062378();
    if (temp_r0 != 0x21) {
        return temp_r0;
    }
    native_fn_020620e8(0x20, 1);
    temp_r4 = native_fn_020cf26c();
    return native_fn_020cba38(temp_r4, native_fn_020cc76c());
}
