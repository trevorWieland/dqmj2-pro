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
extern u32 native_fn_01ffb8bc(void);
extern u32 native_fn_02027f30(u32);
extern u32 native_fn_020443ec(void);
extern u32 native_fn_020845ac(void);
extern u32 native_fn_020c225c(u32);
extern u32 native_data_01fff948;
extern u32 native_data_01fff94c;
extern u8 native_data_021cebe0[];
void native_itcm_01ffa4b4(void) {
    u32 var_r0;
    u32 temp_r2;

    if (native_fn_020443ec() == 8) {
        return;
    }
    if (M2C_FIELD(native_data_021cebe0, s32 *, 0x30) == 1) {
        var_r0 = native_fn_01ffb8bc();
        native_data_01fff948 = 0x12C;
    } else {
        var_r0 = native_fn_020845ac();
        native_data_01fff948 = 0x96;
    }
    if (native_fn_02027f30(0U) == 0) {
        return;
    }
    if (var_r0 == -2U) {
        if (M2C_FIELD(native_data_021cebe0, s32 *, 0x30) == 1) {
            native_fn_020c225c(0x30000000U);
        } else {
            native_fn_020c225c(0x10000000U);
        }
    }
    if (var_r0 == 0) {
        temp_r2 = native_data_01fff94c + 1;
        native_data_01fff94c = temp_r2;
        if (temp_r2 <= (u32) native_data_01fff948) {
            return;
        }
        native_data_01fff94c = 0;
        if (M2C_FIELD(native_data_021cebe0, s32 *, 0x30) == 1) {
            native_fn_020c225c(0x30000000U);
            return;
        }
        native_fn_020c225c(0x10000000U);
        return;
    }
    native_data_01fff94c = 0;
}
