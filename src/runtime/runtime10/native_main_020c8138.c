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
extern u32 native_fn_02041510();
extern u32 native_fn_02041538();
extern u32 native_fn_02047ff0();
extern u32 native_fn_02048034();
extern u32 native_fn_02048f7c();
extern u32 native_fn_0205dc70();
extern u32 native_fn_0205e7a8();
extern u32 native_fn_0205e814();
extern u32 native_fn_020629e0();
extern u32 native_fn_02062a10();
extern u32 native_fn_02062a50();
extern u32 native_fn_02062aa0();
extern u32 native_fn_02063b40();
extern u32 native_fn_02063fa0();
extern u32 native_fn_02063fac();
extern u32 native_fn_02067748();
extern u32 native_fn_02067c60();
extern u32 native_fn_02068f60();
extern u32 native_fn_020698f4();
extern u32 native_fn_0206a04c();
extern u32 native_fn_0206a05c();
extern u32 native_fn_0206bf44();
extern u32 native_fn_0206c484();
extern u32 native_fn_0206dcd0();
extern u32 native_fn_02072f48();
extern u32 native_fn_020c484c();
extern u32 native_fn_020c48bc();
extern u32 native_fn_020c48d0();
extern u32 native_fn_020c48e8();
extern u32 native_fn_020c5a3c();
extern u32 native_fn_020c617c();
extern u32 native_fn_020c8070();
extern u32 native_fn_020c8ef0();
extern u32 native_fn_020c957c();
extern u8 native_data_021d6384[];
extern u8 native_data_021d63c8[];
u32 native_main_020c8138(s32 *arg0) {
    u32 temp_r0;
    u32 temp_r0_2;
    u32 temp_r0_3;
    s8 var_r4;
    s32 var_r5;
    u32 temp_r6;

    var_r5 = 0;
    var_r4 = M2C_FIELD(native_data_021d63c8, s8 *, 0x10);
    *arg0 = 0;
    switch (M2C_FIELD(native_data_021d63c8, s8 *, 0x10)) {
    default:
        break;
    case 0:
        switch (M2C_FIELD(native_data_021d63c8, u32 *, 0)) {
        default:
            break;
        case 0:
            native_fn_0205e7a8(-1, 0x52);
            var_r4 = 1;
            M2C_FIELD(native_data_021d6384, s32 *, 8) = 1;
            break;
        case 1:
            if (native_fn_02063b40(0x11D) == 0) {
                native_fn_020c48bc();
                native_fn_020c48d0(9, 7, 6);
                native_fn_020c48e8(-1);
                native_fn_02048f7c(1);
                native_fn_020c484c();
                native_fn_020c957c(0);
                native_fn_0205e7a8(-1, 0x54);
                M2C_FIELD(native_data_021d6384, s8 *, 5) = 6;
            } else {
                native_fn_0205e7a8(-1, 0x52);
                M2C_FIELD(native_data_021d6384, s32 *, 8) = 1;
                var_r4 = 0xA;
            }
            break;
        case 2:
            native_fn_0205e7a8(-1, 0x52);
            M2C_FIELD(native_data_021d6384, s32 *, 8) = 1;
            var_r4 = 2;
            break;
        case 3:
            native_fn_0205e7a8(-1, 0x52);
            M2C_FIELD(native_data_021d6384, s32 *, 8) = 1;
            var_r4 = 9;
            break;
        case 4:
            if (native_fn_02063b40(0x11E) == 0) {
                native_fn_020c48bc();
                native_fn_020c48d0(9, 7, 7);
                native_fn_020c48e8(-1);
                native_fn_02048f7c(1);
                native_fn_020c484c();
                native_fn_020c957c(0);
                native_fn_0205e7a8(-1, 0x54);
                M2C_FIELD(native_data_021d6384, s8 *, 5) = 6;
            } else {
                native_fn_02041510(1, 2, 0xA);
                native_fn_02041538(1, 2, 0xA);
                native_fn_0205e814(0, 0, 0xA);
                M2C_FIELD(native_data_021d6384, s8 *, 5) = 0xB;
                native_fn_0205e7a8(-1, 0x52);
            }
            break;
        case 5:
            if (native_fn_02062aa0() == 0) {
                native_fn_0205e7a8(-1, 0x54);
            } else {
                native_fn_0205e7a8(-1, 0x53);
                M2C_FIELD(native_data_021d6384, s8 *, 5) = 0xC;
                M2C_FIELD(native_data_021d6384, s32 *, 8) = 1;
            }
            break;
        }
        break;
    case 1:
        temp_r0 = native_fn_020698f4(0);
        switch (temp_r0) {
        case 0:
            temp_r6 = native_fn_0206a04c();
            if ((native_fn_02063b40(0x13) == 0) && (temp_r6 == 1)) {
                M2C_FIELD(native_data_021d6384, s8 *, 5) = 6;
                native_fn_020c48bc();
                native_fn_020c48d0(9, 1, 0x1A);
                native_fn_020c48e8(-1);
                native_fn_02068f60(0);
                native_fn_02048f7c(1);
                native_fn_020c484c();
            } else if (temp_r6 == 2) {
                M2C_FIELD(native_data_021d6384, s8 *, 5) = 6;
                native_fn_020c48bc();
                native_fn_020c48d0(5, 6, 0x2A);
                native_fn_020c48e8(-1);
                native_fn_02068f60(0);
                native_fn_02048f7c(1);
                native_fn_020c484c();
            } else if (native_fn_0206a05c() == 2) {
                native_fn_020c48d0(0xF, 4, 0x38);
                native_fn_02048034(native_fn_0205dc70(0xF, 2, (u16) (M2C_FIELD((void *) native_fn_02067748(), s32 *, 4) + 0x3B)), 0);
                var_r5 = 1;
            } else if (native_fn_0206a05c() == 3) {
                native_fn_020c48d0(0xF, 4, 0x19);
                native_fn_02048034(native_fn_0205dc70(0xF, 2, (u16) (M2C_FIELD((void *) native_fn_02067748(), s32 *, 4) + 0x3B)), 0);
                var_r5 = 1;
            }
            if (var_r5 != 0) {
                M2C_FIELD(native_data_021d6384, s8 *, 5) = 6;
                native_fn_020c48bc();
                native_fn_020c48e8(-1);
                native_fn_02048f7c(1);
                native_fn_020c484c();
                native_fn_02068f60(0);
            }
            break;
        case 1:
            native_fn_0206bf44();
            native_fn_0205e7a8(-1, 0x52);
            native_fn_020c8070();
            if (M2C_FIELD(native_data_021d6384, u8 *, 1) == 1) {
                M2C_FIELD(native_data_021d6384, s8 *, 5) = 0xC;
                native_fn_0206c484(0);
            } else {
                M2C_FIELD(native_data_021d6384, s32 *, 8) = 1;
                var_r4 = 0;
            }
            break;
        case 2:
            if (native_fn_020c617c() != 0) {
                M2C_FIELD(native_data_021d6384, s8 *, 5) = 6;
                native_fn_020c8ef0();
            } else {
                native_fn_0206c484(0);
                M2C_FIELD(native_data_021d6384, s8 *, 5) = 0xC;
            }
            break;
        }
        break;
    case 2:
        temp_r0_2 = native_fn_020c5a3c();
        M2C_FIELD(native_data_021d6384, u32 *, 0x24) = temp_r0_2;
        if (M2C_FIELD(native_data_021d6384, u8 *, 1) == 3) {
            if ((temp_r0_2 != 0) && (native_fn_02063fa0() == 0) && (native_fn_02063fac(M2C_FIELD(native_data_021d6384, u32 *, 0x24)) == 0) && (native_fn_02067c60(M2C_FIELD(native_data_021d6384, u32 *, 0x24)) != 0)) {
                M2C_FIELD(native_data_021d6384, s8 *, 5) = 7;
            } else {
                native_fn_0205e7a8(-1, 0x54);
            }
        } else if (temp_r0_2 != 0) {
            native_fn_0205e7a8(-1, 0x52);
            M2C_FIELD(native_data_021d6384, s32 *, 8) = 1;
            var_r4 = 3;
        } else {
            native_fn_0205e7a8(-1, 0x54);
        }
        break;
    case 3:
        temp_r0_3 = native_fn_02062a10(M2C_FIELD(native_data_021d6384, u32 *, 0x24));
        switch (M2C_FIELD(native_data_021d63c8, u32 *, 0)) {
        case 0:
            if (native_fn_02072f48(M2C_FIELD(temp_r0_3, s16 *, 0x18)) == 0) {
                native_fn_0205e7a8(-1, 0x52);
                native_fn_02041538(1, 2, 0xA);
                var_r4 = 4;
            } else {
                native_fn_0205e7a8(-1, 0x54);
            }
            break;
        case 1:
            native_fn_0205e7a8(-1, 0x52);
            native_fn_02041538(1, 2, 0xA);
            var_r4 = 8;
            break;
        case 2:
            if (((native_fn_02062aa0() == 1) && (M2C_FIELD(native_data_021d6384, u32 *, 0x24) == M2C_FIELD((void *) native_fn_02062a50(0), s32 *, 0x14))) || (native_fn_020629e0() == 1)) {
                native_fn_020c48bc();
                native_fn_020c48d0(9, 1, 0x14);
                native_fn_020c48e8(0x57);
                M2C_FIELD(native_data_021d6384, s8 *, 5) = 6;
                native_fn_0205e7a8(-1, 0x54);
                native_fn_020c48e8(-1);
            } else {
                native_fn_0205e7a8(-1, 0x52);
                var_r4 = 5;
            }
            break;
        }
        break;
    case 5:
        switch (M2C_FIELD(native_data_021d63c8, u32 *, 0)) {
        case 0:
            native_fn_02047ff0(native_fn_02062a10(M2C_FIELD(native_data_021d6384, u32 *, 0x24)), 0x14, 0);
            native_fn_020c48bc();
            native_fn_020c48d0(9, 1, 0x13);
            M2C_FIELD(native_data_021d6384, s8 *, 5) = 9;
            var_r4 = 2;
            native_fn_020c957c(0);
            native_fn_0206dcd0(0);
            native_fn_0205e7a8(-1, 0x52);
            break;
        case 1:
            native_fn_020c957c(0);
            var_r4 = 3;
            native_fn_0205e7a8(-1, 0x53);
            break;
        }
        break;
    case 7:
        if (M2C_FIELD(native_data_021d63c8, u32 *, 0) != 0) {
            native_fn_0205e7a8(-1, 0x53);
            M2C_FIELD(native_data_021d6384, s8 *, 5) = 0xC;
        }
        break;
    }
    return (u32) var_r4;
}
