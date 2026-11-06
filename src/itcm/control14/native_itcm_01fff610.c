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
extern u32 native_fn_01ff9fa0(void);
extern u32 native_fn_01ffa010(void);
extern u32 native_fn_01ffa394(u32);
extern u32 native_fn_01ffa824(void);
extern u32 native_fn_01ffa84c(void);
extern u32 native_fn_01ffa8c8(void);
extern u32 native_fn_01ffa8d8(void);
extern u32 native_fn_01ffb4ec(u32);
extern u32 native_fn_01fff43c(u32, u32, u32, u32);
extern u32 native_fn_020443d4(u32);
extern u32 native_fn_02062a10(u32);
extern u32 native_fn_020633b0(void);
extern u32 native_fn_02064978(void);
extern u32 native_fn_020649ac(u32);
extern u32 native_fn_020649c0(u32);
extern u32 native_fn_020649d4(u32);
extern u32 native_fn_020649e8(u32);
extern u32 native_fn_02064d64(u32, u32, u32);
extern u32 native_fn_02065170(u32, u32, u32);
extern u32 native_fn_020652dc(u32);
extern u32 native_fn_02065304(u32);
extern u32 native_fn_02065608(u32);
extern u32 native_fn_02065630(u32);
extern u32 native_fn_02065648(u32);
extern u32 native_fn_ov000_02223c54();
extern u32 native_fn_ov000_02224700();
u32 native_itcm_01fff610(u32 arg0, u32 arg1, u32 arg2, u32 arg3) {
    u32 temp_r0;
    u32 temp_r0_2;
    u32 temp_r0_3;
    void *temp_r0_4;
    s32 var_r4;
    u32 temp_r4;
    u8 temp_r4_2;
    s32 var_r5;
    u32 temp_r5;
    s32 var_r6;
    u32 temp_r7;
    u32 temp_r7_2;
    u32 var_r7;
    u32 var_r8;
    s32 var_r9;
    u32 temp_r10;
    u32 temp_r10_2;

    temp_r4 = native_fn_ov000_02223c54();
    temp_r5 = native_fn_020633b0();
    native_fn_02064978();
    native_fn_020443d4(2U);
    native_fn_020652dc(0x68U);
    native_fn_02065304(0U);
    native_fn_02065608(native_fn_01ffa8c8());
    native_fn_02065630(1U);
    native_fn_02065648(0x2DU);
    if ((native_fn_01ff9fa0() == 0) && (M2C_FIELD(temp_r4, s8 *, 0x58) == 1)) {
        temp_r4_2 = M2C_FIELD((void *) native_fn_01ffb4ec((u32) (u8) native_fn_01ffa824()), u8 *, 0x166);
        if ((native_fn_01ffa8d8() == 4) && (*(u8 *) native_fn_01ffa010() == 1) && (temp_r4_2 & 4)) {
            native_fn_02065648(0x2BU);
        }
        if ((native_fn_01ffa8d8() == 8) && (*(u8 *) native_fn_01ffa010() == 2) && (temp_r4_2 & 4) && (temp_r4_2 & 2)) {
            native_fn_02065648(0x2BU);
        }
        if (native_fn_01ffa394(native_fn_01ffa84c()) == 0) {
            native_fn_02065630(0U);
        }
    }
    var_r6 = 0;
    var_r9 = 0;
    do {
        var_r7 = 0;
        var_r8 = 0;
        temp_r0 = M2C_FIELD((temp_r5 + (var_r6 * 4)), u32 *, 0x1C);
        if (var_r6 < 3) {
            temp_r0_2 = native_fn_02062a10(temp_r0);
            if (temp_r0_2 != 0) {
                var_r7 = M2C_FIELD(temp_r0_2, u32 *, 0x34);
                var_r8 = M2C_FIELD(temp_r0_2, u32 *, 0x38);
            }
            temp_r10 = native_fn_01ffb4ec((u32) (u8) native_fn_01ffa824());
            native_fn_01fff43c(temp_r10 + 0x14 + var_r9, native_fn_020649ac((u32) var_r6), var_r7, var_r8);
        } else {
            temp_r0_3 = native_fn_02062a10(temp_r0);
            if (temp_r0_3 != 0) {
                var_r7 = M2C_FIELD(temp_r0_3, u32 *, 0x34);
                var_r8 = M2C_FIELD(temp_r0_3, u32 *, 0x38);
            }
            temp_r10_2 = native_fn_01ffb4ec((u32) (u8) native_fn_01ffa824());
            native_fn_01fff43c(temp_r10_2 + 0x14 + var_r9, native_fn_020649d4(var_r6 - 3), var_r7, var_r8);
        }
        var_r6 += 1;
        var_r9 += 0x34;
    } while (var_r6 < 6);
    native_fn_ov000_02224700((u8) native_fn_01ffa824());
    if ((native_fn_01ffa394(native_fn_01ffa84c()) == 0) && (native_fn_01ff9fa0() == 0)) {
        temp_r0_4 = (void *) native_fn_01ffb4ec(native_fn_01ffa84c());
        native_fn_02064d64((u32) M2C_FIELD(temp_r0_4, s16 *, 0x18), (u32) M2C_FIELD(temp_r0_4, s16 *, 0x4C), (u32) M2C_FIELD(temp_r0_4, s16 *, 0x80));
        return native_fn_02065170(-1U, -1U, -1U);
    }
    var_r5 = 0;
    var_r4 = 0;
    do {
        if (var_r5 < 3) {
            temp_r7 = native_fn_01ffb4ec(native_fn_01ffa84c());
            native_fn_01fff43c(temp_r7 + 0x14 + var_r4, native_fn_020649c0((u32) var_r5), 0U, 0U);
        } else {
            temp_r7_2 = native_fn_01ffb4ec(native_fn_01ffa84c());
            native_fn_01fff43c(temp_r7_2 + 0x14 + var_r4, native_fn_020649e8(var_r5 - 3), 0U, 0U);
        }
        var_r5 += 1;
        var_r4 += 0x34;
    } while (var_r5 < 6);
    native_fn_01ffa84c();
    return native_fn_ov000_02224700();
}
