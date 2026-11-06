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
extern u8 native_data_020de57c[];
extern u8 native_data_021c6d80[];
void native_main_0207ff68(void) {
    s32 temp_r0;

    temp_r0 = M2C_FIELD(native_data_021c6d80, s32 *, 4) + 1;
    M2C_FIELD(native_data_021c6d80, s32 *, 4) = temp_r0;
    if (temp_r0 <= 0xA) {
        goto block_2;
    }
    M2C_FIELD(native_data_021c6d80, s32 *, 4) = 0;
    *native_data_020de57c = 1;
    return;
block_2:
    if (temp_r0 != 5) {
        goto block_4;
    }
    *native_data_020de57c = 1;
block_4:
    return;
}
