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
extern u32 native_fn_02065d88();
extern u32 native_fn_ov001_021d9494();
extern u32 ov001_side_slot_record_021db438();
extern u32 ov001_record_is_active_021db8d0();
extern u32 native_fn_ov001_021dbf98();
extern u32 native_fn_ov001_021e1708();
extern u32 native_fn_ov001_021ee78c();
extern u32 native_fn_ov001_021f949c();
extern u32 native_fn_ov001_0220d468();
void native_ov001_0220c3f4(u32 arg0, u32 arg1, u32 arg2) {
    void *temp_r0;
    s32 var_r6;
    s8 temp_r7;
    u32 temp_r8;
    u32 var_r10;
    s32 var_r11;
    s32 sp14;
    s32 sp10;
    s32 spC;

    var_r10 = arg0;
    temp_r0 = (void *) native_fn_02065d88(arg2);
    sp10 = (s32) M2C_FIELD(temp_r0, u8 *, 0x31);
    spC = (s32) M2C_FIELD(temp_r0, u8 *, 0x33);
    if (M2C_FIELD(temp_r0, u8 *, 0x30) != 1) {
        sp14 = 1;
    } else {
        var_r10 = ov001_side_slot_record_021db438(arg1, 0);
        sp14 = 3;
    }
    var_r11 = 0;
    if ((sp14 > 0) && (sp14 > 0)) {
        do {
            if (ov001_record_is_active_021db8d0((void *) var_r10) != 0) {
                native_fn_ov001_021d9494((void *) var_r10, 0, 0);
                temp_r7 = M2C_FIELD((void *) native_fn_02065d88(arg2), s8 *, 0x2A);
                temp_r8 = native_fn_ov001_0220d468(arg2);
                if ((M2C_FIELD(var_r10, u8 *, 0x31E) == 0) || (native_fn_ov001_021e1708(sp10, spC, 0, (void *) var_r10, 0, 0, 0) != 0)) {
                    var_r6 = 0;
                    do {
                        if (temp_r8 & (1 << var_r6)) {
                            native_fn_ov001_021dbf98((void *) var_r10, var_r6, temp_r7, 0, 0);
                        }
                        var_r6 += 1;
                    } while (var_r6 < 0x20);
                } else {
                    native_fn_ov001_021ee78c((void *) var_r10, 0, 0, 1, 0);
                    native_fn_ov001_021f949c(0xF2, 1);
                }
            }
            var_r11 += 1;
            var_r10 += 0x440;
        } while (var_r11 < sp14);
    }
}
