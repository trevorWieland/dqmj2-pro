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
extern u32 native_fn_020c8fc4();
extern u8 native_data_ov000_0222feb4[];
typedef struct {
    u8 unknown_0[0x18];
    s8 field_18;
} Record_native_data_ov000_022468b8;
extern Record_native_data_ov000_022468b8 native_data_ov000_022468b8;
void native_ov000_02227044(void) {
    s8 temp_r0;

    temp_r0 = *(native_data_ov000_0222feb4 + (native_data_ov000_022468b8.field_18 * 5));
    switch (temp_r0) {
    case 3:
        native_fn_020c8fc4(0xA);
        return;
    case 4:
        native_fn_020c8fc4(2);
        return;
    }
}
