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
extern u32 native_fn_0202a634();
extern u32 native_fn_ov001_021f949c();
extern u32 native_fn_ov001_02201504();
extern u32 native_fn_ov001_02201728();
extern u32 native_fn_ov001_02201744();
extern u32 native_fn_ov001_02202360();
extern u32 native_fn_ov001_02203000();
typedef struct {
    u8 unknown_0[0xa];
    s8 field_a;
    u8 unknown_b[0x1];
    s8 field_c;
    u8 unknown_d[0x1];
    s8 field_e;
} Record_native_data_ov001_02239c10;
extern Record_native_data_ov001_02239c10 native_data_ov001_02239c10;
u32 native_ov001_02201438(void) {
    u32 temp_r4;

    temp_r4 = native_fn_0202a634();
    native_fn_ov001_02202360(native_data_ov001_02239c10.field_c);
    if (M2C_FIELD(temp_r4, u16 *, 2) & 0x800) {
        switch (native_data_ov001_02239c10.field_e) {
        case 0:
            native_fn_ov001_02201504();
            native_data_ov001_02239c10.field_a = 8;
            native_fn_ov001_021f949c(0x57, 1);
            break;
        case 1:
            native_fn_ov001_02201728();
            native_data_ov001_02239c10.field_a = 0xC;
            native_fn_ov001_021f949c(0x52, 1);
            break;
        case 2:
            if (native_fn_ov001_02203000() != 0) {
                native_fn_ov001_02201744();
                native_data_ov001_02239c10.field_a = 0x15;
                native_fn_ov001_021f949c(0x52, 1);
            } else {
                native_fn_ov001_021f949c(0x54, 1);
            }
            break;
        }
    }
    return 0U;
}
