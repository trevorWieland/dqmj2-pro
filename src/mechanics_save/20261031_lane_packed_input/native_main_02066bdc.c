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
extern u32 native_fn_02066ae0(void);
extern u32 native_fn_02066b30(void);
typedef struct {
    u8 unknown_0[0x8];
    u8 field_8;
    u8 field_9;
    u8 field_a;
} Record_native_data_021c36bc;
extern Record_native_data_021c36bc native_data_021c36bc;
u32 native_main_02066bdc(void) {
    u8 *temp_r0_2;
    u32 temp_r0;

    temp_r0_2 = (u8 *)native_fn_02066ae0();
    native_data_021c36bc.field_9 = (u8) M2C_FIELD(temp_r0_2, u16 *, 0);
    native_data_021c36bc.field_a = (u8) M2C_FIELD(temp_r0_2, u16 *, 2);
    temp_r0 = native_fn_02066b30();
    native_data_021c36bc.field_8 = (u8)temp_r0;
    return (temp_r0 & 255U) | (native_data_021c36bc.field_9 << 8) | (native_data_021c36bc.field_a << 0x10);
}
