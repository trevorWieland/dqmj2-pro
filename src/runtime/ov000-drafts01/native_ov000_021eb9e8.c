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
    u8 unknown_0[0x10];
    s32 field_10;
    u8 unknown_14[0xc];
    s8 field_20;
} Record_native_data_ov000_02236980;
extern Record_native_data_ov000_02236980 native_data_ov000_02236980;
u32 native_ov000_021eb9e8(u32 arg0) {
    u32 var_r0;

    var_r0 = arg0;
    switch (native_data_ov000_02236980.field_20) {
    case 2:
        var_r0 = 1;
        
    default:
        return var_r0;
    case 0:
        switch (native_data_ov000_02236980.field_10) {
        case 2:
            var_r0 = 2;
            
        default:
            return var_r0;
        case 0:
            return 0U;
        case 1:
            return 1U;
        }
        break;
    case 1:
        return 0U;
    }
}
