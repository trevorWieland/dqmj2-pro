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
extern u32 native_fn_020620b4();
extern u32 native_fn_ov000_021f08c4();
extern u32 native_fn_ov000_021f097c();
extern u8 native_data_ov000_02236d98[];
u32 native_ov000_021f07b8(void) {
    s32 temp_r0;
    u32 temp_r0_2;
    u32 var_r4;
    void *temp_r5;

    temp_r5 = M2C_FIELD(native_data_ov000_02236d98, void **, 8);
    temp_r0 = M2C_FIELD(temp_r5, s32 *, 4);
    var_r4 = M2C_FIELD(temp_r5, u32 *, 0);
    switch (temp_r0) {
    case 0:
        native_fn_ov000_021f08c4();
        native_fn_020620b4(0xA);
        M2C_FIELD(temp_r5, s32 *, 4) = 1;
        break;
    case 1:
        temp_r0_2 = native_fn_ov000_021f097c();
        if (temp_r0_2 != var_r4) {
            M2C_FIELD(temp_r5, s32 *, 0xC) = (s32) M2C_FIELD(temp_r5, s32 *, 0);
            M2C_FIELD(temp_r5, s32 *, 4) = 2;
            M2C_FIELD(temp_r5, u32 *, 8) = temp_r0_2;
        }
        break;
    case 2:
        var_r4 = M2C_FIELD(temp_r5, u32 *, 8);
        native_fn_020620b4(0x10);
        M2C_FIELD(temp_r5, s32 *, 4) = 0;
        break;
    }
    return var_r4;
}
