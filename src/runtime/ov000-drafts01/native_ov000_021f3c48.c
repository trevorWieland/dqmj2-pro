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
extern u32 native_fn_02042464();
extern u32 native_fn_ov000_021f3b58();
extern u32 native_fn_ov000_021f3ba8();
extern u32 native_fn_ov000_021f3c30();
typedef struct {
    u8 unknown_0[0x4];
    s32 field_4;
} Record_native_data_ov000_02236ed8;
extern Record_native_data_ov000_02236ed8 native_data_ov000_02236ed8;
u32 native_ov000_021f3c48(u32 arg0) {
    s32 temp_r0;
    s32 temp_r0_2;
    s32 temp_r5;
    void *temp_r6;

    temp_r0 = (s32) native_fn_ov000_021f3b58();
    if (temp_r0 >= 0) {
        temp_r5 = temp_r0 * 0x27C;
        temp_r6 = native_data_ov000_02236ed8.field_4 + temp_r5;
        if (native_fn_ov000_021f3ba8(temp_r6, arg0) != 0) {
            temp_r0_2 = (s32) native_fn_ov000_021f3c30(arg0, 0);
            if (temp_r0_2 <= 0) {
                M2C_FIELD(temp_r6, s32 *, 0x164) = 0;
            } else {
                native_fn_02042464(temp_r6, temp_r0_2, 1);
            }
            M2C_FIELD((native_data_ov000_02236ed8.field_4 + temp_r5), s8 *, 0x279) = 1;
        }
    }
    return (u32) temp_r0;
}
