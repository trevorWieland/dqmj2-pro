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
extern u32 native_fn_02003b8c();
typedef struct {
    u32 field_0;
    u8 unknown_4[0xc];
    s32 field_10;
} Record_native_data_020e333c;
extern Record_native_data_020e333c native_data_020e333c;
u32 native_main_020057ec(void) {
    u32 temp_r0;

    temp_r0 = native_fn_02003b8c();
    native_data_020e333c.field_0 = temp_r0;
    switch (temp_r0) {
    case 2:
    case 3:
        native_data_020e333c.field_10 = 0x06800000;
        return 0x06800000U;
    case 8:
    case 12:
        native_data_020e333c.field_10 = 0x06840000;
        return 0x06840000U;
    case 1:
        native_data_020e333c.field_10 = 0x067E0000;
        return 0x067E0000U;
    case 4:
        native_data_020e333c.field_10 = 0x06820000;
        return 0x06820000U;
    case 0:
    case 5:
    case 6:
    case 7:
    case 9:
    case 10:
    case 11:
        return temp_r0;
    
default:
        return temp_r0;
    }
}
