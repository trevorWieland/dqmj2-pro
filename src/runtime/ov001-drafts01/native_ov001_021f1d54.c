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
extern u32 native_fn_02041f74();
extern u32 native_fn_02042c2c();
extern u32 native_fn_ov001_021d75d4();
extern u32 native_fn_ov001_021d77b0();
extern u32 native_fn_ov001_021d7814();
extern u32 native_fn_ov001_021d94cc();
extern u32 native_fn_ov001_021db9e0();
extern u32 native_fn_ov001_021dbaac();
extern u8 native_data_ov001_0223989c[];
u32 native_ov001_021f1d54(s32 arg0) {
    u32 temp_r4;
    u8 temp_r5;

    temp_r5 = M2C_FIELD(M2C_FIELD(native_data_ov001_0223989c, void **, 0x84), u8 *, 0x31E);
    temp_r4 = native_fn_ov001_021db9e0();
    if (native_fn_ov001_021dbaac(M2C_FIELD(native_data_ov001_0223989c, void **, 0x84)) != 0) {
        if (arg0 == 5) {
            if (temp_r5 == 0) {
                native_fn_ov001_021d75d4(0x29);
            } else {
                native_fn_ov001_021d75d4(0x25);
            }
        } else if (temp_r5 == 0) {
            native_fn_ov001_021d75d4(0x21);
        } else {
            native_fn_ov001_021d75d4(0x1D);
        }
    } else if (temp_r4 == 2) {
        if (arg0 == 5) {
            if (temp_r5 == 0) {
                native_fn_ov001_021d75d4(0x28);
            } else {
                native_fn_ov001_021d75d4(0x24);
            }
        } else if (temp_r5 == 0) {
            native_fn_ov001_021d75d4(0x20);
        } else {
            native_fn_ov001_021d75d4(0x1C);
        }
    } else if (temp_r4 == 1) {
        if (arg0 == 5) {
            if (temp_r5 == 0) {
                native_fn_ov001_021d75d4(0x27);
            } else {
                native_fn_ov001_021d75d4(0x23);
            }
        } else if (temp_r5 == 0) {
            native_fn_ov001_021d75d4(0x1F);
        } else {
            native_fn_ov001_021d75d4(0x1B);
        }
    } else if (arg0 == 5) {
        if (temp_r5 == 0) {
            native_fn_ov001_021d75d4(0x26);
        } else {
            native_fn_ov001_021d75d4(0x22);
        }
    } else if (temp_r5 == 0) {
        native_fn_ov001_021d75d4(0x1E);
    } else {
        native_fn_ov001_021d75d4(0x1A);
    }
    native_fn_ov001_021d77b0(-1, native_fn_02042c2c(M2C_FIELD(native_data_ov001_0223989c, void **, 0x84)));
    native_fn_ov001_021d7814(-1, native_fn_02041f74(M2C_FIELD(native_data_ov001_0223989c, void **, 0x84), 0));
    if (M2C_FIELD(M2C_FIELD(native_data_ov001_0223989c, void **, 0x84), u8 *, 0x31E) == 0) {
        return native_fn_ov001_021d94cc(1, 0);
    }
    return native_fn_ov001_021d94cc(0, 1);
}
