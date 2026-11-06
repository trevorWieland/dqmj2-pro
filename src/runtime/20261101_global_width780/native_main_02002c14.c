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
#define NULL ((void *)0)
extern u16 native_data_020dcb40[];
extern u16 native_data_020e3300[];
u32 native_main_02002c14(void) {
    u32 temp_r0;
    u32 temp_ip;

    temp_ip = *(u32 *)0x04000000;
    *native_data_020dcb40 = 0;
    *native_data_020e3300 = (s16) ((u32) (temp_ip & 0x30000) >> 0x10);
    temp_r0 = temp_ip & ~0x30000;
    *(u32 *)0x04000000 = temp_r0;
    return temp_r0;
}
