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
extern u32 native_fn_02005b50();
extern u32 native_fn_02005d20();
extern u32 native_fn_02007970();
extern u32 native_fn_02007a34();
extern u8 native_data_020e36f4[];
u32 native_main_020079ac(void) {
    if (M2C_FIELD(native_data_020e36f4, u16 *, 0) != 0) {
        return (u32) M2C_FIELD(native_data_020e36f4, u16 *, 0);
    }
    M2C_FIELD(native_data_020e36f4, u16 *, 0) = 1U;
    native_fn_02007970(0);
    M2C_FIELD(native_data_020e36f4, s32 *, 8) = 0;
    M2C_FIELD(native_data_020e36f4, s32 *, 0xC) = 0;
    M2C_FIELD((void *)0x04000102, s16 *, 0) = 0;
    M2C_FIELD((void *)0x04000102, s16 *, -2) = 0;
    M2C_FIELD((void *)0x04000102, s16 *, 0) = 0xC1;
    native_fn_02005b50(8, native_fn_02007a34);
    native_fn_02005d20(8);
    M2C_FIELD(native_data_020e36f4, s32 *, 4) = 0;
    return (u32) native_data_020e36f4;
}
