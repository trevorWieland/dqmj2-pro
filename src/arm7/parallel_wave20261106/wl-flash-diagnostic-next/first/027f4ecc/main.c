#include "context000.h"

#include "context001.h"

#include "context002.h"

u32 native_host_arm7_main_027f4ecc(void)
{
    u32 length;
    native_host_arm7_arm_0380398c(((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->lockID);
    native_host_arm7_main_027f4ddc();
    length = 0;
    native_host_arm7_arm_027f55c4((u32)(&((LPFLASH_TABLE)0x002a)->tableSize) , 2, (u8 *)&length);
    native_host_arm7_arm_038039e8(((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->lockID);
    if ((length < (sizeof(FLASH_TABLE) - sizeof(((LPFLASH_TABLE)0x002a)->rfInit_channelDependData)) ) || (length > (0x200 - 0x002a) )) {
        ;
        return 0 ;
    }
    length += 2;
    ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->pFlashImg = (void *)native_host_arm7_arm_037f886c(&((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->HeapMan.TmpBuf, length);
    if (((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->pFlashImg == (0) ) {
        return 0 ;
    }
    ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->pFlashImg = (void *)((u32)((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->pFlashImg + (12/2) * 2);
    native_host_arm7_arm_0380398c(((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->lockID);
    native_host_arm7_main_027f4ddc();
    native_host_arm7_arm_027f55c4(0x002a , length, ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->pFlashImg);
    native_host_arm7_arm_038039e8(((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->lockID);
    return 1 ;
}
