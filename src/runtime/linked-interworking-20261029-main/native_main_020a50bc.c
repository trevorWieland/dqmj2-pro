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
extern u32 native_fn_0201b248();
extern u32 native_fn_020a4910();
extern u32 native_fn_020a4938();
extern u32 native_fn_020a4950();
extern u32 native_fn_020a4990();
extern u8 native_data_020dc518[];
u32 native_main_020a50bc(void *arg0) {
    u8 temp_r0;
    u8 temp_r0_2;
    u8 sp0[4];

    temp_r0 = M2C_FIELD(arg0, u8 *, 0xE7);
    if (temp_r0 == 0xFF) {
        return 1U;
    }
    if ((u32) temp_r0 > 2U) {
        return 0U;
    }
    if (native_fn_020a4938(arg0 + 0x40) == 0) {
        return 0U;
    }
    if (native_fn_0201b248(arg0 + 0xC0, native_data_020dc518, 4) != 0) {
        if (native_fn_020a4990(arg0 + 0xC4) == 0) {
            return 0U;
        }
        temp_r0_2 = M2C_FIELD(arg0, u8 *, 0xD0);
        if ((u32) temp_r0_2 > 0x20U) {
            return 0U;
        }
        native_fn_020a4910(temp_r0_2, &sp0);
        if (native_fn_020a4950(arg0 + 0xC0, &sp0) == 0) {
            return 0U;
        }
        goto block_13;
    }
block_13:
    if ((native_fn_0201b248(arg0 + 0xC8, native_data_020dc518, 4) != 0) && (native_fn_020a4990(arg0 + 0xC8) == 0) && (native_fn_020a4990(arg0 + 0xCC) == 0)) {
        return 0U;
    }
    return 1U;
}
