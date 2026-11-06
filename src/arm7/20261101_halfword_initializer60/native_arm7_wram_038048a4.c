typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_host_arm7_data_03809eac[];
extern u16 native_host_arm7_data_03809eb0[];
u32 native_arm7_wram_038048a4(void) {
    s32 temp_r1;
    s32 var_r3;

    M2C_FIELD(native_host_arm7_data_03809eac, u32 *, 0) = 1;
    var_r3 = 0;
    M2C_FIELD(native_host_arm7_data_03809eac, s32 *, 0x24) = 0;
    do {
        temp_r1 = var_r3;
        var_r3 += 1;
        native_host_arm7_data_03809eb0[temp_r1] = 0;
    } while (var_r3 < 0x10);
    return (u32) native_host_arm7_data_03809eb0;
}
