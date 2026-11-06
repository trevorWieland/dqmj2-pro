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
extern u32 native_fn_02048034();
extern u32 native_fn_0205dc70();
extern u32 native_fn_0205e7a8();
extern u32 native_fn_02067748();
extern u32 native_fn_02068f60();
extern u32 native_fn_0206a0fc();
extern u32 native_fn_0206a49c();
extern u32 native_fn_0206a4ac();
extern u32 native_fn_0206c0b0();
extern u32 native_fn_0206c0e0();
extern u32 native_fn_020c1540();
extern u32 native_fn_020c17b0();
extern u32 native_fn_020c485c();
extern u32 native_fn_020cc75c();
extern u32 native_fn_020cd4e8();
extern u32 native_fn_020cd958();
extern u32 native_fn_020cd9ac();
extern u8 native_data_021d6964[];
u32 native_main_020cdbdc(void) {
    s32 temp_r0_2;
    u32 temp_r0_3;
    u32 temp_r0_4;
    u8 temp_r0;
    u32 var_r5;
    s32 var_r6;

    var_r5 = 0;
    temp_r0 = (u8) native_fn_020c1540();
    if (temp_r0 == 0) {
        temp_r0_2 = native_fn_0206a0fc(0) - 1;
        switch (temp_r0_2) {
        case 0:
            native_fn_020cd958();
            native_fn_0205e7a8(-1, 0x52);
            var_r5 = 1;
            break;
        case 1:
            native_fn_020cd9ac();
            native_fn_0205e7a8(-1, 0x53);
            var_r5 = 1;
            break;
        default:
            temp_r0_3 = native_fn_0206a49c();
            if (temp_r0_3 == 1) {
                native_fn_020cd4e8(0xE, -1);
                native_fn_020c485c();
                native_fn_02068f60(0);
                M2C_FIELD(native_data_021d6964, s32 *, 0xC) = 2;
            } else if (temp_r0_3 == 2) {
                native_fn_0205e7a8(-1, 0x54);
            }
            if (native_fn_020cc75c() == 2) {
                var_r6 = 0;
                temp_r0_4 = native_fn_0206a4ac();
                if (temp_r0_4 == 2) {
                    native_fn_02048034(native_fn_0205dc70(9, 8, (u16) (M2C_FIELD((void *) native_fn_02067748(), s32 *, 4) + 0xE)), 0);
                    native_fn_020cd4e8(0x12, -1);
                    var_r6 = 1;
                } else if (temp_r0_4 == 3) {
                    native_fn_020cd4e8(0x2E, -1);
                    var_r6 = 1;
                }
                if (var_r6 != 0) {
                    native_fn_020c485c();
                    native_fn_02068f60(0);
                    M2C_FIELD(native_data_021d6964, s32 *, 0xC) = 2;
                }
            }
            break;
        }
    }
    if ((native_fn_0206c0b0() == 0) && (native_fn_0206c0e0() == 0) && (native_fn_020c17b0() == 0) && (temp_r0 == 0)) {

    } else {
        var_r5 = 1;
    }
    return var_r5;
}
