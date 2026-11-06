typedef unsigned int u32;
extern u32 native_host_arm7_arm_03804c7c(u32);
extern u32 native_host_arm7_arm_03804c00(u32,u32);
u32 native_arm7_wram_03804cf0(u32 mask) {
    u32 value = native_host_arm7_arm_03804c7c(0);
    return native_host_arm7_arm_03804c00(0,value | mask);
}
