typedef unsigned int u32;
typedef signed int s32;
extern u32 native_utility_child_arm7_arm_037fe41c(void);
extern u32 native_utility_child_arm7_arm_037fe430(u32);
extern s32 native_utility_child_arm7_data_03805b78;
extern u32 native_utility_child_arm7_data_03805b7c;
u32 native_utility_child_arm7_wram_037fddcc(s32 sample)
{
    u32 interrupts = native_utility_child_arm7_arm_037fe41c();
    if (sample < native_utility_child_arm7_data_03805b78)
        native_utility_child_arm7_data_03805b7c++;
    native_utility_child_arm7_data_03805b78 = sample;
    native_utility_child_arm7_arm_037fe430(interrupts);
    return native_utility_child_arm7_data_03805b7c;
}
