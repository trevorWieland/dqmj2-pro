#define NULL ((void *)0)
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
extern u8 native_data_ov000_02246600[];
extern u8 native_data_ov000_02246680[];
u32 native_ov000_02223ec0(s32 arg0) {
    void *temp_r1;
    u8 *temp_r2;
    s8 var_ip;

    var_ip = 0;
    native_data_ov000_02246680[arg0] = 0;
    temp_r2 = &native_data_ov000_02246600[arg0];
    do {
        temp_r1 = M2C_FIELD(((arg0 * 0xC) + (s32) native_data_ov000_02246600 + (var_ip * 4)), void **, 0x5C);
        if ((temp_r1 != NULL) && (M2C_FIELD(temp_r1, s16 *, 0x18) != 0)) {
            M2C_FIELD(temp_r2, s8 *, 0x80) = (s8) (M2C_FIELD(temp_r2, s8 *, 0x80) + 1);
        }
        var_ip += 1;
    } while ((s32) var_ip < 3);
    return (u32) (s8) native_data_ov000_02246680[arg0];
}
