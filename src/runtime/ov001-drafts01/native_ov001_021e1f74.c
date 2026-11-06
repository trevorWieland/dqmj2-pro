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
extern u32 native_fn_0207d8e4();
extern u32 native_fn_ov001_02210ad0();
typedef struct {
    u8 unknown_0[0x18];
    u8 field_18;
    u8 field_19;
} Record_native_data_ov001_022388ec;
extern Record_native_data_ov001_022388ec native_data_ov001_022388ec;
extern u8 native_data_ov001_0223893c[];
u32 native_ov001_021e1f74(void *arg0, u32 arg1, u32 *arg2, u32 *arg3) {
    u32 temp_r0;
    u32 temp_r0_2;
    u32 temp_r0_3;
    u8 temp_r0_4;

    temp_r0_3 = native_fn_ov001_02210ad0(arg0, 0x64, native_fn_0207d8e4(M2C_FIELD(arg0, u8 *, 0x1FD)));
    if (temp_r0_3 == 0) {
        return temp_r0_3;
    }
    temp_r0_4 = M2C_FIELD(arg0, u8 *, 0x31E);
    if (temp_r0_4 == 0) {
        *(temp_r0_4 + (native_data_ov001_0223893c + ((native_data_ov001_022388ec.field_18 + *arg2) * 2))) = M2C_FIELD(arg0, u8 *, 0x31F);
        temp_r0_2 = *arg2 + 1;
        *arg2 = temp_r0_2;
        return temp_r0_2;
    }
    *(temp_r0_4 + (native_data_ov001_0223893c + ((native_data_ov001_022388ec.field_19 + *arg3) * 2))) = M2C_FIELD(arg0, u8 *, 0x31F);
    temp_r0 = *arg3 + 1;
    *arg3 = temp_r0;
    return temp_r0;
}
