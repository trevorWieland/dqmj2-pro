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
extern u32 native_fn_0205d790();
extern u32 ov001_side_slot_record_021db438();
extern u32 ov001_record_is_active_021db8d0();
extern u32 native_fn_ov001_021e9cd8();
typedef struct {
    u8 unknown_0[0x24];
    u8 field_24;
} Record_native_data_ov001_02238d7c;
extern Record_native_data_ov001_02238d7c native_data_ov001_02238d7c;
void native_ov001_021ea398(u32 arg0, s32 arg1) {
    u32 temp_r4;
    s32 var_r5;
    s32 var_r6;
    u32 var_r8;

    var_r8 = arg0;
    temp_r4 = native_fn_0205d790(arg1);
    if (var_r8 != 0) {
        var_r5 = 1;
    } else {
        var_r8 = ov001_side_slot_record_021db438(native_data_ov001_02238d7c.field_24, 0);
        var_r5 = 3;
    }
    var_r6 = 0;
    if (var_r5 <= 0) {
        return;
    }
    do {
        if ((ov001_record_is_active_021db8d0((void *) var_r8) != 0) && (arg1 == M2C_FIELD(var_r8, u16 *, 0x34A))) {
            native_fn_ov001_021e9cd8(arg1, (void *) var_r8, temp_r4);
        }
        var_r6 += 1;
        var_r8 += 0x440;
    } while (var_r6 < var_r5);
}
