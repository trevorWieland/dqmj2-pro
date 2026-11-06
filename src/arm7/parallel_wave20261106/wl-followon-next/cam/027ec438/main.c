#include "context000.h"

#include "context001.h"

void native_host_arm7_main_027ec438(u16 camAdrs)
{
    native_host_arm7_arm_027f0d6c(camAdrs);
    ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Config.pCAM[camAdrs].state = 0x00 ;
    ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->CamMan.Count--;
}
