#include "native_node_types.h"
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_host_arm7_arm_037f886c(u32, u32);
extern u32 native_host_arm7_data_0380fff4[];
void native_arm7_main_027e8c78(void *arg0) {
    u8 *temp_r4;
    void *temp_r5;

    temp_r4 = (u8 *)*native_host_arm7_data_0380fff4;
    M2C_FIELD(temp_r4, s32 *, 0x17C) = (s32) M2C_FIELD(arg0, s32 *, 0);
    temp_r5 = temp_r4 + 0x344;
    M2C_FIELD(temp_r4, s32 *, 0x180) = (s32) M2C_FIELD(arg0, s32 *, 4);
    M2C_FIELD(temp_r4, s32 *, 0x184) = (s32) M2C_FIELD(arg0, s32 *, 8);
    native_host_arm7_arm_027e8c5c((u32)(temp_r4 + 0x188), 2U);
    native_host_arm7_arm_027e8c5c((u32)(temp_r4 + 0x194), 3U);
    native_host_arm7_arm_027e8c5c((u32)(temp_r4 + 0x1A0), 4U);
    native_host_arm7_arm_027e8c5c((u32)(temp_r4 + 0x1AC), 5U);
    native_host_arm7_arm_027e8c5c((u32)(temp_r4 + 0x1B8), 6U);
    native_host_arm7_arm_027e8c5c((u32)(temp_r4 + 0x1C4), 7U);
    native_host_arm7_arm_027e8c5c((u32)(temp_r4 + 0x1D0), 8U);
    native_host_arm7_arm_027e8c5c((u32)(temp_r4 + 0x1DC), 9U);
    native_host_arm7_arm_027e8c5c((u32)(temp_r4 + 0x1E8), 0xAU);
    native_host_arm7_arm_027e8c5c((u32)(temp_r4 + 0x1F4), 0xBU);
    native_host_arm7_arm_027e8c5c((u32)(temp_r4 + 0x200), 0xCU);
    M2C_FIELD(temp_r5, s32 *, 0x9C) = (s32) (native_host_arm7_arm_037f886c((u32)(temp_r4 + 0x188), 0x81U) + 0xC);
    M2C_FIELD(temp_r5, s16 *, 0xA0) = 0;
    M2C_FIELD(temp_r5, s16 *, 0xA4) = 0;
}
