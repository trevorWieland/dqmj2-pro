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
extern u32 native_fn_02008430();
extern u32 native_fn_0202a44c();
typedef struct {
    u8 unknown_0[0x2];
    s8 field_2;
    u8 unknown_3[0x19];
    u32 field_1c;
    u8 unknown_20[0x4];
    u32 field_24;
} Record_native_data_ov000_022463b0;
extern Record_native_data_ov000_022463b0 native_data_ov000_022463b0;
void native_ov000_0221f46c(void) {
    u32 temp_r0;

    native_data_ov000_022463b0.field_2 = 0;
    if ((native_data_ov000_022463b0.field_1c == 0) && (native_data_ov000_022463b0.field_24 == 0)) {
        native_data_ov000_022463b0.field_1c = native_fn_0202a44c(2, 0x108, 4);
        temp_r0 = native_fn_0202a44c(2, 0x84, 4);
        native_data_ov000_022463b0.field_24 = temp_r0;
        if ((native_data_ov000_022463b0.field_1c != 0) && (temp_r0 != 0)) {
            return;
        }
        native_fn_02008430();
    }
}
