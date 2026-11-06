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
extern u32 native_fn_02061944(void);
extern u32 native_fn_0206238c(s8 *, s32, s32);
extern u8 native_data_021c4f60[];
extern u8 native_data_021c4f61[];
void native_main_0206f79c(void) {
    u32 temp_r4;

    temp_r4 = native_fn_02061944();
    M2C_FIELD(native_data_021c4f60, u8 *, 0) = (u8) native_fn_0206238c((s8 *)native_data_021c4f61, 1, 6);
    if ((s8) M2C_FIELD(native_data_021c4f60, u8 *, 0) == 1) {
        goto block_2;
    }
    M2C_FIELD(native_data_021c4f60, u8 *, 0) = 0;
block_2:
    if (M2C_FIELD(native_data_021c4f60, s8 *, 1) == M2C_FIELD(temp_r4, s8 *, 0x269)) {
        goto block_4;
    }
    M2C_FIELD(temp_r4, s8 *, 0x26A) = 4;
block_4:
    return;
}
