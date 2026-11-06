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
extern u32 native_fn_ov006_021f23f4();
extern u32 native_fn_ov006_021f52cc();
extern u32 native_fn_ov006_021fc75c();
extern u32 native_fn_ov006_021fc838();
extern u32 native_fn_ov006_021febc4();
extern u32 native_fn_ov006_021ff6d4();
extern u32 native_fn_ov006_021ff718();
extern u32 native_fn_ov006_02200344();
typedef struct {
    u8 field_0;
    u8 unknown_1[0x1];
    u16 field_2;
} Record_native_data_ov006_0221c108;
extern Record_native_data_ov006_0221c108 native_data_ov006_0221c108;
u32 native_ov006_021fc668(void) {
    u32 temp_r0;
    u32 var_r0;
    s32 var_r2;
    void *var_r3;
    void *sp4;

    native_data_ov006_0221c108.field_2 = (u16) (native_data_ov006_0221c108.field_2 + 1);
    var_r0 = 0x12C;
    if ((u32) native_data_ov006_0221c108.field_2 >= 0x12CU) {
        native_fn_ov006_021ff718();
        temp_r0 = native_fn_ov006_021febc4(&sp4);
        if (temp_r0 == 0) {
            native_data_ov006_0221c108.field_0 = 2;
            native_fn_ov006_02200344(0xF, 1, 1, -1, 0);
            native_fn_ov006_021ff6d4(0x12);
            native_fn_ov006_021f23f4();
            return native_fn_ov006_021f52cc(native_fn_ov006_021fc838);
        }
        var_r2 = 0;
        if ((s32) temp_r0 > 0) {
            var_r3 = sp4;
loop_5:
            if (M2C_FIELD(var_r3, u8 *, 0x28) == 2) {
                var_r2 += 1;
                var_r3 += 0x2A;
                if (var_r2 < (s32) temp_r0) {
                    goto loop_5;
                }
            }
        }
        if (var_r2 == temp_r0) {
            native_data_ov006_0221c108.field_0 = 3;
            native_fn_ov006_02200344(0xE, 1, 1, -1, 0);
            native_fn_ov006_021ff6d4(0x12);
            native_fn_ov006_021f23f4();
            return native_fn_ov006_021f52cc(native_fn_ov006_021fc838);
        }
        native_data_ov006_0221c108.field_0 = 1;
        native_fn_ov006_021ff6d4(0xF);
        var_r0 = native_fn_ov006_021f52cc(native_fn_ov006_021fc75c);
        
        return var_r0;
    }
    return var_r0;
}
