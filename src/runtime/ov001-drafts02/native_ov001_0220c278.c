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
extern u32 native_fn_ov001_021ee7d4();
extern u32 native_fn_ov001_022024d4();
extern u32 native_fn_ov001_0220d368();
extern u32 native_fn_ov001_0220d584();
void native_ov001_0220c278(u32 arg0, u32 arg1, u32 arg2) {
    u32 var_r5;
    s32 var_r8;
    s32 var_r9;
    u32 var_r10;

    var_r5 = arg0;
    if (M2C_FIELD((void *) native_fn_02065d88(arg2), u8 *, 0x30) != 1) {
        var_r9 = 1;
    } else {
        var_r5 = ov001_side_slot_record_021db438(arg1, 0);
        var_r9 = 3;
    }
    var_r8 = 0;
    if ((var_r9 > 0) && (var_r9 > 0)) {
        do {
            if (ov001_record_is_active_021db8d0((void *) var_r5) != 0) {
                native_fn_ov001_021d9494((void *) var_r5, 0, 0);
                var_r10 = native_fn_ov001_0220d584((void *) var_r5, arg2);
                if ((s32) var_r10 < 0) {
                    var_r10 = 0;
                }
                native_fn_ov001_021ee7d4((void *) var_r5, (s32) var_r10, native_fn_ov001_0220d368(arg2));
                native_fn_ov001_022024d4(M2C_FIELD(var_r5, u8 *, 0x31E), M2C_FIELD(var_r5, u8 *, 0x31F), 0 - var_r10);
            }
            var_r8 += 1;
            var_r5 += 0x440;
        } while (var_r8 < var_r9);
    }
}
