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
extern u32 native_fn_02049ad0();
extern u32 native_fn_0205dbc4();
extern u32 native_fn_ov000_02202630();
extern u32 native_fn_ov000_02215078();
extern u32 native_fn_ov000_022162b4();
extern u32 native_fn_ov000_022162c0();
extern u32 native_fn_ov000_02216664();
extern u32 native_fn_ov000_02217440();
extern u32 native_fn_ov000_02217a54();
extern u8 native_data_ov000_02237d90[];
extern u8 native_data_ov000_02237d94[];
extern u8 native_data_ov000_02237d9c[];
extern u8 native_data_ov000_02237e8c[];
extern u8 native_data_ov000_02237f34[];
u32 native_ov000_02201eb8(void) {
    u32 temp_r4;

    temp_r4 = native_fn_ov000_02217440();
    switch (*(u32 *)native_data_ov000_02237d94) {
    case 1:
        native_fn_ov000_02216664(native_data_ov000_02237d9c);
        break;
    case 3:
        native_fn_ov000_02216664(native_data_ov000_02237e8c);
        native_fn_02049ad0(1);
        native_fn_ov000_022162c0();
        native_fn_ov000_02215078(native_data_ov000_02237f34, 1);
        break;
    }
    native_fn_ov000_02202630();
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
    native_fn_0205dbc4(2, native_data_ov000_02237d90);
    return 0U;
}
