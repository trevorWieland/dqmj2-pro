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
extern u32 native_fn_0202a634();
extern u32 native_fn_0205e7a8();
extern u32 native_fn_02081400();
extern u8 native_data_020de580[];
extern u8 native_data_021c6dfc[];
extern u8 native_data_021c6e10[];
u32 native_main_020808cc(void) {
    u16 temp_r0;
    u16 temp_r1;
    u16 temp_r1_2;
    void *temp_r0_2;
    void *temp_r4;

    temp_r4 = native_data_021c6e10 + (native_fn_02081400(M2C_FIELD(native_data_021c6dfc, s8 *, 1)) * 0x10);
    temp_r0_2 = (void *) native_fn_0202a634();
    temp_r1 = M2C_FIELD(temp_r0_2, u16 *, 6);
    if (temp_r1 & 0x10) {
        M2C_FIELD(native_data_021c6dfc, s8 *, 5) = (s8) (M2C_FIELD(native_data_021c6dfc, s8 *, 5) + 1);
        if ((s32) M2C_FIELD(native_data_021c6dfc, s8 *, 5) > (s32) (M2C_FIELD(temp_r4, s32 *, 8) - 1)) {
            M2C_FIELD(native_data_021c6dfc, s8 *, 5) = 0;
        }
    } else if (temp_r1 & 0x20) {
        M2C_FIELD(native_data_021c6dfc, s8 *, 5) = (s8) (M2C_FIELD(native_data_021c6dfc, s8 *, 5) - 1);
        if ((s32) M2C_FIELD(native_data_021c6dfc, s8 *, 5) < 0) {
            M2C_FIELD(native_data_021c6dfc, s8 *, 5) = (s8) (M2C_FIELD(temp_r4, s32 *, 8) - 1);
        }
    }
    temp_r1_2 = M2C_FIELD(temp_r0_2, u16 *, 6);
    if (temp_r1_2 & 0x80) {
        if (M2C_FIELD(native_data_021c6dfc, s8 *, 1) == 4) {
            M2C_FIELD(native_data_021c6dfc, s8 *, 1) = 6;
            M2C_FIELD(native_data_021c6dfc, s8 *, 5) = 0;
        } else {
            M2C_FIELD(native_data_021c6dfc, s8 *, 1) = (s8) (M2C_FIELD(native_data_021c6dfc, s8 *, 1) + 1);
            if ((s32) M2C_FIELD(native_data_021c6dfc, s8 *, 1) > 6) {
                M2C_FIELD(native_data_021c6dfc, s8 *, 1) = 1;
            }
        }
    } else if (temp_r1_2 & 0x40) {
        if (M2C_FIELD(native_data_021c6dfc, s8 *, 1) == 6) {
            M2C_FIELD(native_data_021c6dfc, s8 *, 1) = 4;
        } else {
            M2C_FIELD(native_data_021c6dfc, s8 *, 1) = (s8) (M2C_FIELD(native_data_021c6dfc, s8 *, 1) - 1);
            if ((s32) M2C_FIELD(native_data_021c6dfc, s8 *, 1) < 1) {
                M2C_FIELD(native_data_021c6dfc, s8 *, 1) = 6;
                M2C_FIELD(native_data_021c6dfc, s8 *, 5) = 0;
            }
        }
    }
    temp_r0 = M2C_FIELD(temp_r0_2, u16 *, 6);
    if (!(temp_r0 & 0xF0)) {
        return (u32) temp_r0;
    }
    native_fn_0205e7a8(-1, 0x55);
    *native_data_020de580 = 1;
    return (u32) native_data_020de580;
}
