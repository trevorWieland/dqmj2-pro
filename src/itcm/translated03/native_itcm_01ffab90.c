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
extern u32 native_fn_01ffb34c();
extern u32 native_fn_02048a60();
extern u32 native_fn_02049ae4();
extern u32 native_fn_0205f98c();
extern u32 native_fn_0205f9e4();
extern u8 native_data_01fff960[];
extern u8 native_data_021cebe0[];
u8 native_data_01fff960[0x48];

u32 native_itcm_01ffab90(void) {
    u32 temp_r0;
    u32 temp_r4;
    void *temp_r2;

    native_fn_01ffb34c();
    native_fn_0205f9e4();
    if ((s32) M2C_FIELD(native_data_021cebe0, s8 *, 4) > 0) {
        M2C_FIELD(native_data_021cebe0, s8 *, 4) = (s8) (M2C_FIELD(native_data_021cebe0, s8 *, 4) - 1);
        if (M2C_FIELD(native_data_021cebe0, s8 *, 4) == 0) {
            temp_r4 = native_fn_0205f98c(M2C_FIELD(native_data_01fff960, s32 *, 0x1C), 0);
            temp_r0 = native_fn_02049ae4();
            if (temp_r0 != 0) {
                M2C_FIELD(temp_r4, s32 *, 0x7C) = (s32) (M2C_FIELD(temp_r4, s32 *, 0x7C) | 2);
                temp_r2 = M2C_FIELD(temp_r0, void **, 4);
                native_fn_02048a60(temp_r4, 0xE0, (((M2C_FIELD(temp_r2, u8 *, 0x33) + M2C_FIELD(temp_r2, u8 *, 0x35)) - 3) * 8) + 4);
            }
        }
    }
    return native_fn_0205f9e4(native_data_01fff960);
}
