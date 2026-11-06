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
extern u32 native_fn_020cab98(s32);
typedef struct {
    u8 unknown_0[0x8];
    s32 field_8;
} Record_native_data_021d64cc;
extern Record_native_data_021d64cc native_data_021d64cc;
extern u8 native_data_021d64d8[];
void native_main_020cab38(void) {
    s32 temp_r0;

    temp_r0 = native_data_021d64cc.field_8;
    if (temp_r0 <= 0) {
        return;
    }
    do {
        native_fn_020cab98(M2C_FIELD(&native_data_021d64d8[temp_r0], s8 *, -1));
    } while ((temp_r0 = native_data_021d64cc.field_8) > 0);
    return;
}
