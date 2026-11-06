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
extern u32 native_fn_0205f35c(s32, s32);
extern u32 native_fn_02062e44(s32, s8, const void *);
extern u32 native_fn_02062ee4(s32);
extern u32 native_fn_02062f2c(s32);
extern u32 native_fn_02062f74(s32, u8);
extern u32 native_fn_020630e4(s32, s32);
extern u8 *native_fn_02065d88(int);
extern u32 native_fn_02065dec(s32);
extern u32 native_fn_020756e4(s32, s32, s32);
extern u32 native_fn_ov000_021e7b9c(s32);
extern s32 native_fn_ov000_022140c0(void *, const void *, s32);
extern void *native_fn_ov000_02215698(void);
extern u32 native_fn_ov000_0221573c(s32);
extern u32 native_fn_ov000_02215bc8(void);
extern const u8 *native_fn_ov000_02215d94(u8);
__declspec(align(4)) extern u8 native_data_021c5a24[];
extern u32 native_data_021c5b20;
typedef struct {
    u8 unknown_0[0xd8];
    s16 field_d8;
} Record_native_data_021c6124;
extern Record_native_data_021c6124 native_data_021c6124;
extern void *native_data_021c6210[];
u32 native_main_020731ac(void) {
    u32 *selected_index;
    u32 temp_r0;
    u8 temp_r0_2;
    u8 temp_r0_3;
    u32 temp_r4;
    void *temp_r5;
    u32 var_r6;
    s32 var_r7;
    s16 temp_r8;
    void *temp_r9;
    struct { u8 id; u8 allocated; } slot_input;

    native_fn_ov000_02215698();
    temp_r8 = native_data_021c6124.field_d8;
    selected_index = &native_data_021c5b20;
    var_r6 = 0;
    M2C_FIELD(native_data_021c5a24, s8 *, 0x7D7) = 0;
    if (((u32) (M2C_FIELD(native_data_021c5a24, u8 *, 0x7DA) << 0x1C) >> 0x1C) == 0) {
        temp_r5 = native_data_021c6210[*selected_index];
        if (M2C_FIELD(native_fn_02065d88(temp_r8), u8 *, 0x28) == 0x1A) {
            if (native_fn_02062f74(M2C_FIELD(temp_r5, s32 *, 0x14), (u8) M2C_FIELD(native_fn_02065d88(temp_r8), u16 *, 0x1C)) == 0) {
                temp_r4 = native_fn_02062ee4(M2C_FIELD(temp_r5, s32 *, 0x14));
                if ((s32) temp_r4 < (s32) native_fn_02062f2c(M2C_FIELD(temp_r5, s16 *, 0x18))) {
                    slot_input.id = (s8) M2C_FIELD(native_fn_02065d88(temp_r8), u16 *, 0x1C);
                    slot_input.allocated = 0;
                    native_fn_02062e44(M2C_FIELD(temp_r5, s32 *, 0x14), (s8) temp_r4, &slot_input);
                    M2C_FIELD(native_data_021c5a24, s8 *, 0x7D7) = 0xB;
                    native_fn_ov000_02215bc8();
                    var_r6 = 1;
                } else {
                    M2C_FIELD(native_data_021c5a24, s8 *, 0x7D7) = 0xC;
                    var_r6 = 2;
                }
            }
        } else {
            temp_r0 = native_fn_ov000_022140c0(temp_r5, native_fn_ov000_02215d94((u8) *selected_index), temp_r8);
            if (temp_r0 != -1U) {
                temp_r0_2 = M2C_FIELD(native_fn_02065d88(temp_r8), u8 *, 0x28);
                switch ((s32) temp_r0_2) {
                case 1:
                    M2C_FIELD(native_data_021c5a24, s8 *, 0x7D7) = 1;
                    break;
                case 2:
                    M2C_FIELD(native_data_021c5a24, s8 *, 0x7D7) = 3;
                    break;
                case 3:
                    M2C_FIELD(native_data_021c5a24, s8 *, 0x7D7) = 4;
                    break;
                case 12:
                    M2C_FIELD(native_data_021c5a24, s8 *, 0x7D7) = 5;
                    break;
                case 48:
                    M2C_FIELD(native_data_021c5a24, s8 *, 0x7D7) = 0x24;
                    break;
                case 13:
                case 14:
                case 15:
                case 16:
                case 17:
                case 18:
                    M2C_FIELD(native_data_021c5a24, s8 *, 0x7D7) = 6;
                    break;
                }
                var_r6 = 1;
                M2C_FIELD(native_data_021c5a24, u32 *, 0x7E0) = temp_r0;
            }
        }
        M2C_FIELD(native_data_021c5a24, void **, 0x3CC) = temp_r5;
    } else if (M2C_FIELD(native_fn_02065d88(temp_r8), u8 *, 0x30) == 1) {
        if (M2C_FIELD(native_fn_02065d88(temp_r8), u8 *, 0x28) == 0x14) {
            native_fn_ov000_0221573c(0xD);
            var_r6 = 3;
        } else {
            var_r7 = 0;
            if ((s32) M2C_FIELD(native_data_021c5a24, u8 *, 0x7D6) > 0) {
                do {
                    temp_r9 = M2C_FIELD((native_data_021c5a24 + (var_r7 * 4)), void **, 0x7EC);
                    if (native_fn_ov000_022140c0(temp_r9, native_fn_ov000_02215d94(var_r7), temp_r8) != -1U) {
                        var_r6 = 1;
                        temp_r0_3 = M2C_FIELD(native_fn_02065d88(temp_r8), u8 *, 0x28);
                        switch (temp_r0_3) {
                        case 1:
                            M2C_FIELD(native_data_021c5a24, s8 *, 0x7D7) = 2;
                            break;
                        case 2:
                            M2C_FIELD(native_data_021c5a24, s8 *, 0x7D7) = 3;
                            break;
                        }
                    }
                    var_r7 += 1;
                } while ((s32) var_r7 < (s32) M2C_FIELD(native_data_021c5a24, u8 *, 0x7D6));
            }
        }
    } else if (native_fn_ov000_022140c0(NULL, 0U, temp_r8) != -1U) {
        var_r6 = 1;
        if (M2C_FIELD(native_fn_02065d88(temp_r8), u8 *, 0x28) == 0x18) {
            M2C_FIELD(native_data_021c5a24, s8 *, 0x7D7) = 0xA;
        }
    }
    switch (var_r6) {
    default:
        break;
    case 1:
        if (native_fn_02065dec(temp_r8) != 0) {
            native_fn_020630e4(temp_r8, -1);
        }
        native_fn_0205f35c(-1, 0x9A);
        native_fn_020756e4(-1, -1, 4);
        break;
    case 0:
        native_fn_ov000_021e7b9c(0x54);
        native_fn_020756e4(-1, -1, 4);
        break;
    case 2:
        native_fn_ov000_021e7b9c(0x52);
        native_fn_020756e4(-1, -1, 5);
        M2C_FIELD(native_data_021c5a24, s32 *, 0x1EC) = 0;
        M2C_FIELD(native_data_021c5a24, s32 *, 0x1F0) = 0;
        break;
    case 3:
        if (native_fn_02065dec(temp_r8) != 0) {
            native_fn_020630e4(temp_r8, -1);
        }
        break;
    }
    return var_r6;
}
