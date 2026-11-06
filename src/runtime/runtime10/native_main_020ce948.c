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
extern u32 native_fn_0205e7a8();
extern u32 native_fn_020620b4();
extern u32 native_fn_02062358();
extern u32 native_fn_020c3828();
extern u32 native_fn_020c385c();
extern u32 native_fn_020c3904();
extern u32 native_fn_020cc740();
extern u32 native_fn_020cc76c();
extern u32 native_fn_020cd4e8();
extern u32 native_fn_020ced38();
extern u32 native_fn_020cf26c();
extern u32 native_fn_020cf27c();
extern u32 native_fn_020d13a8();
extern u32 native_fn_020d13bc();
extern u32 native_fn_020d13e0();
extern u8 native_data_021d69a0[];
u32 native_main_020ce948(void *arg0) {
    s32 temp_r0_2;
    u32 temp_r0;
    u16 temp_r1;
    u8 var_r4;
    u8 var_r4_2;
    void *temp_r5;
    u8 var_r6;
    u32 temp_r7;
    u8 var_r8;
    u8 var_r9;

    temp_r0 = native_fn_020cf27c();
    temp_r1 = M2C_FIELD(arg0, u16 *, 2);
    temp_r7 = temp_r0;
    if (temp_r1 & 1) {
        temp_r0_2 = *(s32 *) native_fn_020cc740();
        switch ((u8) temp_r0_2) {
        default:
            return (u32) (u8) temp_r0_2;
        case 0:
            native_fn_020d13a8(1, native_fn_020cc76c());
            native_fn_020620b4(0x21);
            var_r4 = 0;
            do {
                native_fn_020d13bc(var_r4, native_fn_020c3828(var_r4));
                var_r4 += 1;
            } while ((u32) var_r4 < 3U);
            native_fn_020cf26c();
            native_fn_020d13e0();
            native_fn_02062358(1);
            native_fn_020ced38(temp_r7, 0, 0x1D);
            M2C_FIELD(native_data_021d69a0, s32 *, 4) = 2;
            return (u32) native_data_021d69a0;
        case 1:
            var_r8 = 0;
            var_r9 = 0;
            do {
                temp_r5 = temp_r7 + (var_r9 * 4);
                if (M2C_FIELD(temp_r5, s32 *, 0x18) != 0) {
                    var_r6 = 0;
                    do {
                        if (M2C_FIELD(temp_r5, s32 *, 0x18) == native_fn_020c3828(var_r6)) {
                            var_r8 += 1;
                        }
                        var_r6 += 1;
                    } while ((u32) var_r6 < 3U);
                }
                var_r9 += 1;
            } while ((u32) var_r9 < 3U);
            if (var_r8 != native_fn_020c385c()) {
                native_fn_020d13a8(2, native_fn_020cc76c());
                native_fn_020620b4(0x21);
                var_r4_2 = 0;
                do {
                    native_fn_020d13bc(var_r4_2, native_fn_020c3904(var_r4_2));
                    var_r4_2 += 1;
                } while ((u32) var_r4_2 < 3U);
                native_fn_020cf26c();
                native_fn_020d13e0();
                native_fn_02062358(1);
                native_fn_020ced38(temp_r7, 0, 0x1E);
                M2C_FIELD(native_data_021d69a0, s32 *, 4) = 2;
                return (u32) native_data_021d69a0;
            }
            native_fn_020cd4e8(0x21, 0x54);
            M2C_FIELD(native_data_021d69a0, s32 *, 4) = 3;
            return (u32) native_data_021d69a0;
        case 2:
            M2C_FIELD(native_data_021d69a0, s32 *, 4) = 4;
            return native_fn_0205e7a8(-1, 0x52);
        }
    } else {
        if (!(temp_r1 & 2)) {
            return temp_r0;
        }
        M2C_FIELD(native_data_021d69a0, s32 *, 4) = 6;
        return native_fn_0205e7a8(-1, 0x53);
    }
}
