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
    u8 unknown_0[0x8];
    s32 field_8;
} Record_native_data_ov000_02236d98;
extern Record_native_data_ov000_02236d98 native_data_ov000_02236d98;
u32 native_ov000_021f24d8(s32 arg0, s32 arg1) {
    s32 var_ip;
    void *temp_r3;

    var_ip = 0;
loop_1:
    temp_r3 = native_data_ov000_02236d98.field_8 + (var_ip * 4);
    if ((arg0 == M2C_FIELD(temp_r3, s16 *, 0x190C)) && (arg1 == M2C_FIELD(temp_r3, u8 *, 0x190E))) {
        return 1U;
    }
    var_ip += 1;
    if (var_ip >= 3) {
        return 0U;
    }
    goto loop_1;
}
