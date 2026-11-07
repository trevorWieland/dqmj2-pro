void RTC_ReadStatus1(RTCRawStatus1 *stat)
{
    native_host_arm7_arm_037fe5a8(EXI_GPIOIF_GPIO);
    native_host_arm7_arm_027f6ec0(0x86 , 0x00 , stat, 1);
}

void RTC_WriteStatus1(const RTCRawStatus1 *stat)
{
    native_host_arm7_arm_037fe5a8(EXI_GPIOIF_GPIO);
    native_host_arm7_arm_027f6ec0(0x06 , 0x00 , stat, 1);
}

void native_host_arm7_arm_027f6ca0(RTCRawAlarm *alarm);

void native_host_arm7_arm_027f6db0(RTCRawAlarm *alarm);

void native_host_arm7_arm_027f6ec0(u16 inst, u16 param, void *buf, u32 size)
{
    native_host_arm7_arm_027f6f1c();
    native_host_arm7_arm_027f6f90(inst, param);
    switch (inst) {
    case 0x86 :
        RTCi_GpioReceiveData(buf, size);
        break;
    case 0x06 :
        native_host_arm7_arm_027f7010(buf, size);
        break;
    }
    native_host_arm7_arm_027f6f5c();
}
