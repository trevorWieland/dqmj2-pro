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
extern u32 native_fn_02078804();
extern u32 native_fn_02078940();
extern u32 native_fn_ov000_021f34ac();
extern u32 native_fn_ov000_02215bc8();
extern u32 native_fn_ov000_022162b4();
extern u32 native_fn_ov000_02216664();
extern u32 native_fn_ov000_02217440();
extern u32 native_fn_ov000_02217a54();
extern u8 native_data_021c6234[];
extern u8 native_data_021c6240[];
u32 native_main_02077938(void) {
    u32 temp_r4;

    temp_r4 = native_fn_ov000_02217440();
    if (M2C_FIELD(native_data_021c6234, u8 *, 0x2D3) != 1) {
        native_fn_ov000_021f34ac(2);
    }
    native_fn_ov000_02216664(native_data_021c6240);
    native_fn_02078804();
    native_fn_ov000_022162b4(M2C_FIELD(temp_r4, s8 *, 0x10), 0x7F);
    native_fn_ov000_022162b4(M2C_FIELD(temp_r4, s8 *, 0x10), 2);
    native_fn_ov000_022162b4(M2C_FIELD(temp_r4, s8 *, 0x10), 0xC);
    native_fn_ov000_022162b4(M2C_FIELD(temp_r4, s8 *, 0x10), 5);
    native_fn_ov000_022162b4(M2C_FIELD(temp_r4, s8 *, 0x10), 6);
    native_fn_ov000_022162b4(M2C_FIELD(temp_r4, s8 *, 0x10), 7);
    native_fn_ov000_022162b4(M2C_FIELD(temp_r4, s8 *, 0x10), 8);
    native_fn_ov000_022162b4(M2C_FIELD(temp_r4, s8 *, 0x10), 9);
    native_fn_ov000_022162b4(M2C_FIELD(temp_r4, s8 *, 0x10), 0xA);
    native_fn_ov000_022162b4(M2C_FIELD(temp_r4, s8 *, 0x10), 0xD);
    native_fn_ov000_022162b4(M2C_FIELD(temp_r4, s8 *, 0x10), 0xE);
    native_fn_ov000_022162b4(M2C_FIELD(temp_r4, s8 *, 0x10), 0xF);
    native_fn_ov000_02217a54();
    native_fn_02078940();
    if (M2C_FIELD(native_data_021c6234, u8 *, 0x2DD) != 0) {
        native_fn_ov000_02215bc8();
    }
    return 0U;
}
