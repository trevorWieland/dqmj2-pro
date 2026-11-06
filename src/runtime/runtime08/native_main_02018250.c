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
extern u32 native_fn_02011f14();
extern u32 native_fn_02012764();
extern u32 native_fn_02016d74();
extern u32 native_fn_020187cc();
extern u8 native_data_020ec360[];
u32 native_main_02018250(void) {
    u32 temp_r0;

    M2C_FIELD(M2C_FIELD(native_data_020ec360, void **, 8), s16 *, 0x528) = 0;
    M2C_FIELD(M2C_FIELD(native_data_020ec360, void **, 8), s16 *, 0x52A) = 0;
    M2C_FIELD(M2C_FIELD(native_data_020ec360, void **, 8), s16 *, 0x526) = 0;
    M2C_FIELD(M2C_FIELD(native_data_020ec360, void **, 8), s16 *, 0x548) = 0;
    native_fn_020187cc(0xA);
    if (M2C_FIELD(M2C_FIELD(native_data_020ec360, void **, 0xC), s32 *, 0x1320) == 0) {
        do {
            temp_r0 = native_fn_02012764(M2C_FIELD(native_data_020ec360, s32 *, 4), M2C_FIELD(M2C_FIELD(native_data_020ec360, void **, 8), s32 *, 0x508), M2C_FIELD(native_data_020ec360, u16 *, 0));
        } while (temp_r0 == 4);
        if (temp_r0 != 2) {
            return 8U;
        }
        native_fn_02011f14(M2C_FIELD(M2C_FIELD(native_data_020ec360, void **, 8), s32 *, 0x508));
        M2C_FIELD(M2C_FIELD(native_data_020ec360, void **, 8), s8 *, 0x50D) = 1;
        return 0U;
    }
    native_fn_02011f14(M2C_FIELD(M2C_FIELD(native_data_020ec360, void **, 8), s32 *, 0x508));
    M2C_FIELD(M2C_FIELD(native_data_020ec360, void **, 8), s8 *, 0x50D) = 1;
    native_fn_02016d74();
    return 0U;
}
