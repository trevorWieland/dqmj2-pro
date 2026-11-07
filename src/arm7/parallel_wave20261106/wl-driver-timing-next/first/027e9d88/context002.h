u32 BBP_Read(u32 adrs)
{
    *(vu16 *)(0x04808000 + 0x158) = (u16)((0x0006 * (0x0001 << 12)) | (adrs * (0x0001 << 0) ));
    native_host_arm7_arm_037fb420();
    return (u32)(*(vu16 *)(0x04808000 + 0x15C) );
}

u32 native_host_arm7_arm_027ea5fc(u32 adrs, u32 data);

void native_host_arm7_arm_027ea7cc(void);

void native_host_arm7_arm_027ea9a8(void *arg);

void WWait(u16 ms)
{
    WWaitus(ms * 1000);
}

void WWaitus(u32 us)
{
    native_host_arm7_arm_037fb32c(us, native_host_arm7_arm_027ea9a8);
}
