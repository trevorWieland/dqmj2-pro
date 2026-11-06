typedef unsigned int u32;
typedef signed int s32;
extern s32 native_host_arm7_arm_037fe410(u32,u32,u32);
s32 native_arm7_main_027f6074(u32 selector, u32 value) {
    u32 payload = ((selector << 8) & 0x7f00) | 0x8000 | (value & 255);
    s32 result;
    do { result = native_host_arm7_arm_037fe410(5,payload,0); } while (result < 0);
    return result;
}
