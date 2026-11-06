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
u32 native_main_02084508(void *arg0, void *arg1) {
    if ((M2C_FIELD(arg0, u8 *, 0) == M2C_FIELD(arg1, u8 *, 0)) && (M2C_FIELD(arg0, u8 *, 1) == M2C_FIELD(arg1, u8 *, 1)) && (M2C_FIELD(arg0, u8 *, 2) == M2C_FIELD(arg1, u8 *, 2)) && (M2C_FIELD(arg0, u8 *, 3) == M2C_FIELD(arg1, u8 *, 3)) && (M2C_FIELD(arg0, u8 *, 4) == M2C_FIELD(arg1, u8 *, 4)) && (M2C_FIELD(arg0, u8 *, 5) == M2C_FIELD(arg1, u8 *, 5))) {
        return 1U;
    }
    return 0U;
}
