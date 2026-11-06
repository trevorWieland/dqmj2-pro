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
extern u32 native_fn_0202a634();
extern u32 native_fn_0205e7a8(u32, u32);
extern u32 native_fn_02062a50(u32);
extern u32 native_fn_02062a88(u32);
extern u32 native_fn_02062aa0();
extern u32 native_fn_02062b0c();
extern u32 native_fn_02063144(u32);
extern u32 native_fn_02065d88(u32);
extern u32 native_fn_020c48e8(u32);
extern u32 native_fn_ov000_021ed334(u32, u32, u32);
extern u32 native_fn_ov000_021ed63c(u32);
extern u32 native_fn_ov000_021edf44(u32, u32);
extern u32 native_fn_ov000_021ee168(u32);
extern u32 native_fn_ov000_021ef154(u32);
extern u32 native_fn_ov000_021ef17c(u32);
extern u32 native_fn_ov000_021ef3a0(u32);
extern u32 native_fn_ov000_021efe60(u32);
extern u32 native_fn_ov000_021efec4(u32, u32);
extern u32 native_fn_ov000_02211064(u32, u32);
extern u8 native_data_ov000_02236bc4[];
u32 native_ov000_021ed6bc(u8 *arg0) {
    s32 temp_r0;
    s32 temp_r1;
    s32 temp_r5;
    s32 temp_r5_4;
    s8 temp_r2;
    s8 var_r4;
    u32 temp_r0_2;
    u32 temp_r6;
    u32 temp_r6_2;
    u32 temp_r7;
    u32 temp_r7_2;
    u32 var_r0;
    u8 temp_r5_2;
    u8 temp_r5_3;

    var_r4 = M2C_FIELD(M2C_FIELD(native_data_ov000_02236bc4, void **, 4), s8 *, 0x20);
    native_fn_0202a634();
    temp_r2 = M2C_FIELD(M2C_FIELD(native_data_ov000_02236bc4, void **, 4), s8 *, 0x20);
    switch (temp_r2) {
    default:
        break;
    case 0:
        M2C_FIELD(M2C_FIELD(native_data_ov000_02236bc4, void **, 4), s32 *, 0x510) = (s32) M2C_FIELD(M2C_FIELD(native_data_ov000_02236bc4, void **, 4), s32 *, 0x10);
        temp_r0 = M2C_FIELD(M2C_FIELD(native_data_ov000_02236bc4, void **, 4), s32 *, 0x10);
        switch (temp_r0) {
        case 0:
            native_fn_0205e7a8(-1, 0x52);
            var_r4 = 1;
            break;
        case 1:
            if (M2C_FIELD(M2C_FIELD(native_data_ov000_02236bc4, void **, 4), u8 *, 0x504) != 0) {
                var_r4 = 2;
                native_fn_0205e7a8(-1, 0x52);
            } else {
                native_fn_0205e7a8(-1, 0x53);
            }
            break;
        case 2:
            native_fn_0205e7a8(-1, 0x53);
            M2C_FIELD(M2C_FIELD(native_data_ov000_02236bc4, void **, 4), s8 *, 0x100) = 6;
            break;
        }
        break;
    case 1:
        M2C_FIELD(M2C_FIELD(native_data_ov000_02236bc4, void **, 4), s32 *, 0x50C) = (s32) M2C_FIELD((M2C_FIELD(native_data_ov000_02236bc4, void **, 4) + (M2C_FIELD(M2C_FIELD(native_data_ov000_02236bc4, void **, 4), s32 *, 0x10) * 4)), s32 *, 0x104);
        temp_r5 = M2C_FIELD(M2C_FIELD(native_data_ov000_02236bc4, void **, 4), s32 *, 0x50C);
        if (M2C_FIELD((void *) native_fn_02065d88(temp_r5), u8 *, 0x2C) == 7) {
            temp_r6 = native_fn_02063144(temp_r5);
            if ((s32) temp_r6 >= (s32) M2C_FIELD((void *) native_fn_02065d88(temp_r5), u8 *, 0x27)) {
                native_fn_ov000_021ed334(9, 2, 0x15);
                M2C_FIELD(M2C_FIELD(native_data_ov000_02236bc4, void **, 4), s8 *, 0x100) = 4;
                native_fn_0205e7a8(-1, 0x54);
                native_fn_020c48e8(-1);
            } else {
                temp_r6_2 = native_fn_02062b0c();
                if ((s32) temp_r6_2 < (s32) native_fn_ov000_021ed63c(temp_r5)) {
                    native_fn_ov000_021ed334(9, 2, 0x16);
                    M2C_FIELD(M2C_FIELD(native_data_ov000_02236bc4, void **, 4), s8 *, 0x100) = 4;
                    native_fn_0205e7a8(-1, 0x54);
                    native_fn_020c48e8(-1);
                } else {
                    var_r4 = 3;
                    M2C_FIELD(M2C_FIELD(native_data_ov000_02236bc4, void **, 4), s32 *, 0x514) = (s32) M2C_FIELD(M2C_FIELD(native_data_ov000_02236bc4, void **, 4), s32 *, 0x10);
                    native_fn_0205e7a8(-1, 0x52);
                }
            }
        } else if (M2C_FIELD(M2C_FIELD(native_data_ov000_02236bc4, void **, 4), u8 *, 0x101) == 0) {
            temp_r7 = native_fn_02063144(temp_r5);
            if ((s32) temp_r7 >= (s32) M2C_FIELD((void *) native_fn_02065d88(temp_r5), u8 *, 0x27)) {
                native_fn_ov000_021ed334(9, 2, 0x15);
                M2C_FIELD(M2C_FIELD(native_data_ov000_02236bc4, void **, 4), s8 *, 0x100) = 4;
                native_fn_0205e7a8(-1, 0x54);
                native_fn_020c48e8(-1);
            } else {
                temp_r7_2 = native_fn_02062b0c();
                if ((s32) temp_r7_2 < (s32) native_fn_ov000_021ed63c(temp_r5)) {
                    native_fn_ov000_021ed334(9, 2, 0x16);
                    M2C_FIELD(M2C_FIELD(native_data_ov000_02236bc4, void **, 4), s8 *, 0x100) = 4;
                    native_fn_0205e7a8(-1, 0x54);
                    native_fn_020c48e8(-1);
                } else {
                    temp_r5_2 = ((M2C_FIELD(M2C_FIELD(native_data_ov000_02236bc4, void **, 4), s32 *, 0x10) - M2C_FIELD(M2C_FIELD(native_data_ov000_02236bc4, void **, 4), s32 *, 0x14)) * 2) + 8;
                    native_fn_ov000_021efe60(0);
                    native_fn_ov000_021ef17c(0);
                    native_fn_ov000_021efec4(temp_r5_2, (s8) ((M2C_FIELD(M2C_FIELD(native_data_ov000_02236bc4, void **, 4), s32 *, 0x10) - M2C_FIELD(M2C_FIELD(native_data_ov000_02236bc4, void **, 4), s32 *, 0x14)) + 8));
                    M2C_FIELD(M2C_FIELD(native_data_ov000_02236bc4, void **, 4), u8 *, 0x101) = 1U;
                    M2C_FIELD(M2C_FIELD(native_data_ov000_02236bc4, void **, 4), s16 *, 0x506) = 1;
                    native_fn_ov000_021ef154(0);
                    native_fn_0205e7a8(-1, 0x52);
                    *arg0 |= 6;
                }
            }
        } else {
            if (native_fn_ov000_021edf44(temp_r5, M2C_FIELD(M2C_FIELD(native_data_ov000_02236bc4, void **, 4), s16 *, 0x506)) == 0) {
                native_fn_0205e7a8(-1, 0x53);
            }
            M2C_FIELD(M2C_FIELD(native_data_ov000_02236bc4, void **, 4), s8 *, 0x518) = 1;
            native_fn_ov000_021ef3a0(0);
            *arg0 |= 6;
        }
        break;
    case 2:
        if (M2C_FIELD(M2C_FIELD(native_data_ov000_02236bc4, void **, 4), u8 *, 0x101) == 0) {
            temp_r0_2 = native_fn_ov000_021ee168(M2C_FIELD((M2C_FIELD(native_data_ov000_02236bc4, void **, 4) + (M2C_FIELD(M2C_FIELD(native_data_ov000_02236bc4, void **, 4), s32 *, 0x10) * 4)), s32 *, 0x104));
            if (temp_r0_2 == 0) {
                temp_r5_3 = ((M2C_FIELD(M2C_FIELD(native_data_ov000_02236bc4, void **, 4), s32 *, 0x10) - M2C_FIELD(M2C_FIELD(native_data_ov000_02236bc4, void **, 4), s32 *, 0x14)) * 2) + 8;
                native_fn_ov000_021efe60(0);
                native_fn_ov000_021ef17c(0);
                native_fn_ov000_021efec4(temp_r5_3, (s8) ((M2C_FIELD(M2C_FIELD(native_data_ov000_02236bc4, void **, 4), s32 *, 0x10) - M2C_FIELD(M2C_FIELD(native_data_ov000_02236bc4, void **, 4), s32 *, 0x14)) + 8));
                M2C_FIELD(M2C_FIELD(native_data_ov000_02236bc4, void **, 4), u8 *, 0x101) = 1U;
                M2C_FIELD(M2C_FIELD(native_data_ov000_02236bc4, void **, 4), s16 *, 0x506) = 1;
                native_fn_ov000_021ef154(0);
                native_fn_0205e7a8(-1, 0x52);
                *arg0 |= 6;
            } else {
                if (temp_r0_2 == 2) {
                    native_fn_ov000_021ed334(9, 2, 4);
                } else {
                    native_fn_ov000_021ed334(9, 2, 3);
                }
                M2C_FIELD(M2C_FIELD(native_data_ov000_02236bc4, void **, 4), s8 *, 0x100) = 4;
                native_fn_0205e7a8(-1, 0x54);
                native_fn_020c48e8(-1);
            }
        } else {
            if (native_fn_ov000_021edf44(M2C_FIELD((M2C_FIELD(native_data_ov000_02236bc4, void **, 4) + (M2C_FIELD(M2C_FIELD(native_data_ov000_02236bc4, void **, 4), s32 *, 0x10) * 4)), s32 *, 0x104), (s16) (0 - M2C_FIELD(M2C_FIELD(native_data_ov000_02236bc4, void **, 4), s16 *, 0x506))) == 0) {
                native_fn_0205e7a8(-1, 0x53);
            }
            M2C_FIELD(M2C_FIELD(native_data_ov000_02236bc4, void **, 4), s8 *, 0x518) = 1;
            native_fn_ov000_021ef3a0(0);
            *arg0 |= 6;
        }
        break;
    case 3:
        temp_r1 = M2C_FIELD(M2C_FIELD(native_data_ov000_02236bc4, void **, 4), s32 *, 0x10);
        switch (temp_r1) {
        case 0:
            native_fn_0205e7a8(-1, 0x52);
            var_r4 = 4;
            break;
        case 1:
            if (native_fn_ov000_021edf44(M2C_FIELD(M2C_FIELD(native_data_ov000_02236bc4, void **, 4), s32 *, 0x50C), 1) != 0) {
                M2C_FIELD(M2C_FIELD(native_data_ov000_02236bc4, void **, 4), s8 *, 0x518) = 1;
                native_fn_ov000_021ef154(0);
            } else {
                native_fn_0205e7a8(-1, 0x53);
            }
            break;
        case 2:
            var_r4 = 1;
            native_fn_0205e7a8(-1, 0x53);
            break;
        }
        *arg0 |= 7;
        break;
    case 4:
        temp_r5_4 = M2C_FIELD(M2C_FIELD(native_data_ov000_02236bc4, void **, 4), s32 *, 0x10);
        if (temp_r5_4 < (s32) native_fn_02062aa0()) {
            var_r0 = native_fn_02062a50(temp_r5_4);
        } else {
            var_r0 = native_fn_02062a88(M2C_FIELD(M2C_FIELD(native_data_ov000_02236bc4, void **, 4), s32 *, 0x10) - native_fn_02062aa0());
        }
        if (native_fn_ov000_02211064((void *) var_r0, M2C_FIELD((void *) native_fn_02065d88(M2C_FIELD(M2C_FIELD(native_data_ov000_02236bc4, void **, 4), s32 *, 0x50C)), u8 *, 0x2D)) != 0) {
            if (native_fn_ov000_021edf44(M2C_FIELD(M2C_FIELD(native_data_ov000_02236bc4, void **, 4), s32 *, 0x50C), 1) != 0) {
                M2C_FIELD(var_r0, s8 *, 0x31) = (s8) M2C_FIELD(M2C_FIELD(native_data_ov000_02236bc4, void **, 4), s32 *, 0x50C);
                M2C_FIELD(M2C_FIELD(native_data_ov000_02236bc4, void **, 4), s8 *, 0x518) = 1;
                native_fn_ov000_021ef154(0);
                native_fn_0205e7a8(-1, 0x5D);
            } else {
                native_fn_0205e7a8(-1, 0x53);
            }
        } else {
            native_fn_0205e7a8(-1, 0x54);
        }
        *arg0 |= 7;
        break;
    }
    return (u32) var_r4;
}
