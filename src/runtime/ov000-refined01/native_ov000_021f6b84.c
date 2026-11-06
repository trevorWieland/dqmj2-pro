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
extern u32 native_fn_01ffb35c();
extern u32 native_fn_0205e7a8();
extern u32 native_fn_02061270();
extern u32 native_fn_02061944();
extern u32 native_fn_020620b4();
extern u32 native_fn_02062134();
extern u32 native_fn_02062358();
extern u32 native_fn_0206e474();
extern u32 native_fn_0206e6c0();
extern u32 native_fn_ov000_021f6e84();
typedef struct {
    u8 unknown_0[0x8];
    s32 field_8;
    s32 field_c;
} Record_native_data_ov000_02236ee4;
extern Record_native_data_ov000_02236ee4 native_data_ov000_02236ee4;
u32 native_ov000_021f6b84(void) {
    void *temp_r0;
    s8 var_r5;
    u32 var_r6;

    temp_r0 = (void *) native_fn_02061944();
    var_r5 = M2C_FIELD(temp_r0, s8 *, 0x269);
    var_r6 = 0;
    if (native_data_ov000_02236ee4.field_c == 1) {
        native_fn_ov000_021f6e84();
        native_fn_0206e6c0((u8) (var_r5 - 0x1B));
        native_data_ov000_02236ee4.field_c = 0;
    }
    if ((native_fn_02061270() == 0) && (M2C_FIELD(temp_r0, s8 *, 0x26C) == 0x2A)) {
        if (M2C_FIELD((void *) native_fn_01ffb35c(), u16 *, 6) & 0x100) {
            native_fn_02062358(1);
            var_r5 += 1;
            native_fn_0205e7a8(-1, 0x56);
        } else if (M2C_FIELD((void *) native_fn_01ffb35c(), u16 *, 6) & 0x200) {
            native_fn_02062358(0);
            var_r5 -= 1;
            native_fn_0205e7a8(-1, 0x56);
        }
    }
    native_fn_0206e474();
    if ((s32) var_r5 < 0x1B) {
        var_r5 = 0x1C;
    }
    if ((s32) var_r5 > 0x1C) {
        var_r5 = 0x1B;
    }
    if (M2C_FIELD(temp_r0, s8 *, 0x26C) != 0x2A) {
        var_r6 = 1;
    }
    if (var_r5 != M2C_FIELD(temp_r0, s8 *, 0x269)) {
        native_fn_02062134(1);
        native_data_ov000_02236ee4.field_8 = 1;
        native_fn_020620b4((s32) var_r5);
    }
    return var_r6;
}
