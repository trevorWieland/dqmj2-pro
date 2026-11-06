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
typedef struct { u32 value:24; u32 other:8; } PackedResourceWord;
extern u32 native_fn_02038d88(u32);
extern u32 native_fn_02038e50(u32);
extern u32 native_fn_02038eb4(u32);
extern u32 native_fn_0203906c(u32);
extern u32 native_fn_0203917c(u32);
typedef struct {
    u8 unknown_0[0x1];
    u8 field_1;
} Record_native_data_021b8ae0;
extern Record_native_data_021b8ae0 native_data_021b8ae0;
u32 native_main_0205ef8c(s32 arg0) {
    u8 *temp_r0;
    u8 *temp_r0_2;
    s32 var_r4;
    u32 var_r5;
    u8 *temp_r6;

    var_r5 = 0;
    if (arg0 >= 0) {
        temp_r0 = (u8 *)native_fn_02038d88((u32)arg0);
        temp_r6 = (u8 *)native_fn_02038e50(M2C_FIELD(temp_r0, u16 *, 4));
        if (native_fn_0203917c(M2C_FIELD(temp_r0, u32 *, 0)) == 0) {
            var_r5 += native_fn_0203906c(M2C_FIELD(temp_r0, u32 *, 0));
        }
        if (native_fn_0203917c(M2C_FIELD(temp_r6,u32 *,0)) == 0) {
            var_r5 += native_fn_0203906c(M2C_FIELD(temp_r6,u32 *,0));
        }
        var_r4 = 0;
        do {
            if (M2C_FIELD((temp_r6 + (var_r4 * 2)), u16 *, 4) != 0xFFFF) {
                temp_r0_2 = (u8 *)native_fn_02038eb4(M2C_FIELD((temp_r6 + (var_r4 * 2)), u16 *, 4));
                if (native_fn_0203917c(((PackedResourceWord *)temp_r0_2)->value) == 0) {
                    var_r5 += native_fn_0203906c(((PackedResourceWord *)temp_r0_2)->value);
                }
            }
            var_r4 += 1;
        } while (var_r4 < 4);
        if (var_r5 != 0) {
            native_data_021b8ae0.field_1 = 0xDU;
        } else {
            native_data_021b8ae0.field_1 = 0xEU;
        }
    } else {
        native_data_021b8ae0.field_1 = 0xFU;
    }
    return (u32) native_data_021b8ae0.field_1;
}
