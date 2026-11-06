#define NULL ((void *)0)
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
extern u32 native_fn_020270c0();
extern u32 native_fn_0202a1e0();
extern u32 native_fn_02041538();
extern u32 native_fn_02041814();
extern u32 native_fn_02045738();
extern u32 native_fn_0204617c();
extern u32 native_fn_02049940();
extern u32 native_fn_02061944();
extern u32 native_fn_020620e8();
extern u32 native_fn_02062e18();
extern u32 native_fn_020633c8();
extern u32 native_fn_0206dcd0();
extern u32 native_fn_0206de44();
extern u32 native_fn_0206de64();
extern u32 native_fn_02078958();
extern u32 native_fn_0207e874();
extern u32 native_fn_0207e948();
extern u32 native_fn_0207f390();
extern u32 native_fn_0207f3b0();
extern u32 native_fn_020c40e8();
extern u32 native_fn_020c42c8();
extern u32 native_fn_020c4960();
extern u32 native_fn_020c49e8();
extern u32 native_fn_020c59b0();
extern u32 native_fn_020c59e0();
extern u32 native_fn_020c59f4();
extern u32 native_fn_020c5ab8();
extern u32 native_fn_020c7814();
extern u32 native_fn_020c8e48();
extern u32 native_fn_020c8fb4();
extern u32 native_fn_020c9294();
extern u32 native_fn_020c9308();
extern u32 native_fn_020c94a8();
extern u32 native_fn_020c957c();
extern u32 native_fn_020cab38();
extern u32 native_fn_020cab74();
extern u32 native_fn_020cad94();
extern u32 native_fn_020cada0();
extern u32 native_fn_020caedc();
extern u32 native_fn_020cc298();
extern u32 native_fn_020cc2f4();
extern u32 native_fn_ov000_021f0844();
extern u32 native_fn_ov000_021f0fb0();
extern u32 native_fn_ov000_021f2750();
extern u32 native_fn_ov000_021f2c78();
extern u32 native_fn_ov000_02215694();
extern u8 native_data_021d6384[];
typedef struct {
    u8 unknown_0[0x10];
    s8 field_10;
} Record_native_data_021d63c8;
extern Record_native_data_021d63c8 native_data_021d63c8;
u32 native_main_020c7868(void) {
    s32 var_r0_2;
    u8 *var_r0;
    s32 var_r4;
    u32 temp_r4;
    u32 var_r4_2;
    u32 var_r4_3;
    u32 var_r4_4;
    u32 var_r4_5;

    var_r0 = native_data_021d6384;
    var_r4 = 0;
    switch (M2C_FIELD(native_data_021d6384, s8 *, 2)) {
    default:
        break;
    case 0:
        if (native_data_021d63c8.field_10 == 1) {
            native_fn_020c7814();
            native_fn_020cab38();
            M2C_FIELD(native_data_021d6384, u8 *, 6) = 0U;
        } else if (native_data_021d63c8.field_10 == 2) {
            native_fn_020c9294(0);
            var_r4_2 = native_fn_020cada0();
            native_fn_020c59b0();
            native_fn_020c5ab8();
            if ((s32) var_r4_2 > 1) {
                do {
                    native_fn_020cab74();
                    var_r4_2 -= 1;
                } while ((s32) var_r4_2 > 1);
            }
            native_fn_020270c0();
        } else {
            native_fn_020cab38();
        }
        var_r0 = (u8 *) native_fn_020c49e8();
        var_r4 = 1;
        break;
    case 1:
        native_fn_020cab38();
        native_fn_020c49e8();
        var_r0 = (u8 *) native_fn_020c94a8();
        var_r4 = 1;
        break;
    case 2:
        var_r4_3 = native_fn_020cada0();
        if (native_data_021d63c8.field_10 == 0) {
            if ((s32) var_r4_3 > 1) {
                do {
                    native_fn_020cab74();
                    var_r4_3 -= 1;
                } while ((s32) var_r4_3 > 1);
            }
        }
        else if (native_data_021d63c8.field_10 == 5) {
            if ((s32) var_r4_3 > 2) {
                do {
                    native_fn_020cab74();
                    var_r4_3 -= 1;
                } while ((s32) var_r4_3 > 2);
            }
            native_fn_0206dcd0(0);
        }
        else if (native_data_021d63c8.field_10 == 3) {
            if ((s32) var_r4_3 > 2) {
                do {
                    native_fn_020cab74();
                    var_r4_3 -= 1;
                } while ((s32) var_r4_3 > 2);
            }
            if (M2C_FIELD(native_fn_02061944(), s8 *, 0x269) != 1) {
                native_fn_020620e8(1, 1);
            }
        }
        else if (native_data_021d63c8.field_10 == 4) {
            native_fn_ov000_02215694();
            native_fn_020c8e48();
            native_fn_02078958(0);
            native_fn_020c8fb4();
            native_fn_020633c8();
        }
        else {
            native_fn_020cab38();
        }

        native_fn_020c49e8();
        if (native_data_021d63c8.field_10 == 5) {
            native_fn_020c957c(0);
        }
        var_r0 = (u8 *) native_data_021d63c8.field_10;
        if (var_r0 == NULL) {
            var_r0 = (u8 *) native_fn_020c59f4();
        }
        var_r4 = 1;
        break;
    case 3:
        if (native_data_021d63c8.field_10 == 8) {
            if (native_fn_02041814() == 1) {
                var_r0 = (u8 *) native_fn_0207e874();
            } else {
                native_fn_0207e948();
                native_fn_020c8e48();
                if (native_fn_0207f390() != 0) {
                    native_fn_02062e18(M2C_FIELD(native_data_021d6384, s32 *, 0x24), native_fn_0207f3b0());
                    native_fn_0206de44(1);
                    native_fn_0206de64(1);
                }
                native_fn_02041538(0, 2, 0xA);
                native_fn_020cab38();
                var_r0 = (u8 *) native_fn_020c49e8();
                goto block_61;
            }
        } else {
            var_r4_4 = native_fn_020cada0();
            if (native_data_021d63c8.field_10 == 5) {
                if ((s32) var_r4_4 > 3) {
                    do {
                        native_fn_020cab74();
                        var_r4_4 -= 1;
                    } while ((s32) var_r4_4 > 3);
                }
            } else if (native_data_021d63c8.field_10 == 2) {
                native_fn_020c9294(0);
                if ((s32) var_r4_4 > 2) {
                    do {
                        native_fn_020cab74();
                        var_r4_4 -= 1;
                    } while ((s32) var_r4_4 > 2);
                }
                native_fn_020270c0();
            } else {
                native_fn_020cab38();
            }
            native_fn_020c49e8();
            var_r0 = (u8 *) native_data_021d63c8.field_10;
            if (var_r0 == (u8 *)2) {
                native_fn_020c59e0();
                native_fn_020c59b0();
                var_r0 = (u8 *) native_fn_020c5ab8();
            }
block_61:
            var_r4 = 1;
        }
        break;
    case 5:
        var_r4_5 = native_fn_020cada0();
        if (native_data_021d63c8.field_10 == 3) {
            if ((s32) var_r4_5 > 3) {
                do {
                    native_fn_020cab74();
                    var_r4_5 -= 1;
                } while ((s32) var_r4_5 > 3);
            }
        } else {
            native_fn_020cab38();
        }
        native_fn_020c49e8();
        var_r0 = (u8 *) native_fn_020c957c(0);
        var_r4 = 1;
        break;
    case 4:
    case 8:
        if (M2C_FIELD(native_data_021d6384, u8 *, 6) == 0) {
            var_r0_2 = 1;
        } else {
            var_r0_2 = 0;
        }
        native_fn_020c9308(var_r0_2);
        var_r0 = (u8 *) native_fn_02041814();
        if (var_r0 != (u8 *)1) {
            temp_r4 = native_fn_0202a1e0(2U);
            native_fn_020c94a8();
            native_fn_0202a1e0(temp_r4);
            native_fn_020cad94();
            native_fn_020caedc();
            native_fn_020c40e8();
            native_fn_0204617c(1, 2);
            native_fn_0204617c(2, 2);
            var_r0 = (u8 *) native_fn_02045738(1);
            var_r4 = 1;
        }
        break;
    case 9:
        native_fn_020cab38();
        native_fn_020c42c8();
        native_fn_020c49e8();
        native_fn_020c4960();
        native_fn_ov000_021f2c78();
        native_fn_ov000_021f0fb0();
        M2C_FIELD(native_data_021d6384, s8 *, 3) = (s8) native_data_021d63c8.field_10;
        native_data_021d63c8.field_10 = (s8) M2C_FIELD(native_data_021d6384, s8 *, 2);
        M2C_FIELD(native_data_021d6384, s8 *, 5) = 0xA;
        native_fn_ov000_021f2750(0);
        var_r0 = (u8 *) native_fn_ov000_021f0844();
        break;
    case 10:
        native_fn_020cab38();
        native_fn_020c94a8();
        native_fn_020c49e8();
        native_fn_020c4960();
        native_fn_02049940(0);
        native_fn_02049940(1);
        M2C_FIELD(native_data_021d6384, s8 *, 3) = (s8) native_data_021d63c8.field_10;
        native_data_021d63c8.field_10 = (s8) M2C_FIELD(native_data_021d6384, s8 *, 2);
        M2C_FIELD(native_data_021d6384, s8 *, 5) = 0xA;
        native_fn_020cc298();
        var_r0 = (u8 *) native_fn_020cc2f4();
        break;
    }
    if (var_r4 == 0) {
        return (u32) var_r0;
    }
    M2C_FIELD(native_data_021d6384, s8 *, 3) = (s8) native_data_021d63c8.field_10;
    native_data_021d63c8.field_10 = (s8) M2C_FIELD(native_data_021d6384, s8 *, 2);
    M2C_FIELD(native_data_021d6384, s8 *, 5) = 2;
    return (u32) native_data_021d6384;
}
