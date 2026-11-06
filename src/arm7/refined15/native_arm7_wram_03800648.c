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
extern u32 native_arm7_fn_03800b00(u32);
extern u8 native_arm7_data_03808420;
u32 native_arm7_wram_03800648(u32 arg0, u32 arg1) {
    s32 temp_r0;
    s32 var_r5;
    u32 temp_r1;
    void *var_r0;

    var_r5 = 0;
    do {
        temp_r0 = var_r5 * 0x24;
        var_r0 = &native_arm7_data_03808420 + temp_r0;
        if (((u32) (*(&native_arm7_data_03808420 + temp_r0) << 0x1F) >> 0x1F) != 0) {
            temp_r1 = M2C_FIELD(var_r0, u32 *, 0x20);
            if ((arg0 <= temp_r1) && (temp_r1 <= arg1)) {
                var_r0 = (void *) native_arm7_fn_03800b00((u32) var_r0);
            }
        }
        var_r5 += 1;
    } while (var_r5 < 0x10);
    return (u32) var_r0;
}
