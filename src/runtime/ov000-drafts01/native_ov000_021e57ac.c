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
typedef struct {
    u8 unknown_0[0x4];
    u16 field_4;
} Record_native_data_ov000_0223255c;
extern Record_native_data_ov000_0223255c native_data_ov000_0223255c;
extern u8 native_data_ov000_02232868[];
u32 native_ov000_021e57ac(void) {
    s32 var_r1;
    u8 *var_r2;

    var_r2 = native_data_ov000_02232868;
    var_r1 = 0;
loop_1:
    if (M2C_FIELD(var_r2, u16 *, 0) == (u8) native_data_ov000_0223255c.field_4) {
        return (u32) M2C_FIELD(var_r2, u8 *, 3);
    }
    var_r1 += 1;
    var_r2 += 0x14;
    if (var_r1 >= 0x20) {
        return 0U;
    }
    goto loop_1;
}
