typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u8 native_host_arm7_data_03806fa9[160];
#define native_host_arm7_data_03807028 (native_host_arm7_data_03806fa9 + 127)
u32 native_arm7_wram_037fee58(s32 arg0) {
    if (arg0 < 0x20) {
        return (u32) (s8) native_host_arm7_data_03807028[arg0];
    }
    if (arg0 < 0x40) {
        return (u32) (s8) native_host_arm7_data_03807028[0x40 - arg0];
    }
    if (arg0 < 0x60) {
        return (u32) (s8) (0 - (s8) native_host_arm7_data_03807028[arg0 - 0x40]);
    }
    return (u32) (s8) (0 - (s8) native_host_arm7_data_03807028[0x20 - (arg0 - 0x60)]);
}
