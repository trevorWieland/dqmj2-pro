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
extern u32 ov001_side_slot_record_021db438();
extern u32 ov001_record_is_active_021db8d0();
extern u32 native_fn_ov001_021f5078();
void native_ov001_0220cf10(u32 arg0, u32 arg1, u32 arg2) {
    s32 var_r5;
    s32 var_r6;
    u32 var_r7;

    var_r7 = arg0;
    if (M2C_FIELD((void *) native_fn_02065d88(arg2), u8 *, 0x30) != 1) {
        var_r6 = 1;
    } else {
        var_r7 = ov001_side_slot_record_021db438(arg1, 0);
        var_r6 = 3;
    }
    var_r5 = 0;
    if ((var_r6 > 0) && (var_r6 > 0)) {
        do {
            if (ov001_record_is_active_021db8d0(var_r7) != 0) {
                native_fn_ov001_021f5078(0, var_r7);
            }
            var_r5 += 1;
            var_r7 += 0x440;
        } while (var_r5 < var_r6);
    }
}
