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
extern u8 *native_fn_0202a634(void);
typedef struct {
    u8 unknown_0[0x4];
    s32 field_4;
} Record_native_data_020ddb08;
extern Record_native_data_020ddb08 native_data_020ddb08;
s32 native_main_020494bc(s32 *arg0, s32 arg1, s32 arg2, s32 arg3, s32 arg4) {
    u8 *temp_r0;
    s32 var_r1;
    s32 temp_r2;
    s32 var_r3;
    s32 var_r3_2;
    u16 temp_ip;

    temp_r0 = native_fn_0202a634();
    temp_ip = M2C_FIELD(temp_r0, u16 *, 6);
    var_r1 = 0;
    temp_r2 = *arg0;
    if (temp_ip & 0x40) {
        var_r1++;
    }
    if (temp_ip & 0x10) {
        if (arg4 != 0) {
            var_r3 = arg1;
        } else {
            var_r3 = 0xA;
        }
        var_r1 = (s32)((u32)var_r1 + (u32)var_r3);
    }
    if (temp_ip & 0x80) {
        var_r1 = (s32)((u32)var_r1 - 1);
    }
    if (temp_ip & 0x20) {
        if (arg4 != 0) {
            var_r3_2 = (s32)((u32)arg1 - (u32)arg2);
        } else {
            var_r3_2 = 0xA;
        }
        var_r1 = (s32)((u32)var_r1 - (u32)var_r3_2);
    }
    if ((temp_r2 == arg1) && !(M2C_FIELD(temp_r0, u16 *, 0) & 0x60) && (arg3 != 0)) {
        native_data_020ddb08.field_4 = 0;
    }
    if ((*arg0 == arg2) && !(M2C_FIELD(temp_r0, u16 *, 0) & 0x90) && (arg3 != 0)) {
        native_data_020ddb08.field_4 = 0;
    }
    temp_r2 = (s32)((u32)temp_r2 + (u32)var_r1);
    if (var_r1 > 0) {
        if (temp_r2 > arg1) {
            if ((*arg0 == arg1) && (native_data_020ddb08.field_4 == 0)) {
                temp_r2 = arg2;
            } else {
                temp_r2 = arg1;
            }
        } else {
            native_data_020ddb08.field_4 = 1;
        }
    } else if (var_r1 < 0) {
        if (temp_r2 < arg2) {
            if ((*arg0 == arg2) && (native_data_020ddb08.field_4 == 0)) {
                temp_r2 = arg1;
            } else {
                temp_r2 = arg2;
            }
        } else {
            native_data_020ddb08.field_4 = 1;
        }
    }
    *arg0 = temp_r2;
    return var_r1;
}
