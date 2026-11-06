typedef unsigned int u32;
extern void native_host_arm7_arm_027f6f1c(void);
extern void native_host_arm7_arm_027f6f90(u32,u32);
extern void native_host_arm7_arm_027f7010(void *,u32);
extern void native_host_arm7_arm_027f70c8(void *,u32);
extern void native_host_arm7_arm_027f6f5c(void);

void native_arm7_main_027f6ec0(u32 command,u32 qualifier,void *data,u32 count)
{
    native_host_arm7_arm_027f6f1c();
    native_host_arm7_arm_027f6f90(command,qualifier);
    if(command!=6)
    {
        if(command==0x86)
            native_host_arm7_arm_027f70c8(data,count);
    }
    else
        native_host_arm7_arm_027f7010(data,count);
    native_host_arm7_arm_027f6f5c();
}
