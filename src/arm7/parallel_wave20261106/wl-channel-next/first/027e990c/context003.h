u32 CheckEnableChannel(u32 ch)
{
    return ((u32)0x0001 << ch) & ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Config.EnableChannel;
}

u32 native_host_arm7_arm_027ea5fc(u32 adrs, u32 data);

void native_host_arm7_arm_027ea62c(u32 data);
