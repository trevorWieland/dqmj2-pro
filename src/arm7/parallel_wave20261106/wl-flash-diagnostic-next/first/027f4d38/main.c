#include "context000.h"

#include "context001.h"

#include "context002.h"

u32 native_host_arm7_main_027f4d38(u32 *pCrc)
{
    u8 *p;
    u32 crc, rcrc, tbsize, c;
    tbsize = ((FLASH_TABLE *)((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->pFlashImg)->tableSize;
    if ((tbsize < (sizeof(FLASH_TABLE) - sizeof(((LPFLASH_TABLE)0x002a)->rfInit_channelDependData)) ) || (tbsize > (0x200 - 0x002a) )) {
        ;
        return 2;
    }
    p = (u8 *)((u32)((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->pFlashImg + 2);
    crc = 0;
    c = 0;
    for (; tbsize > 0; tbsize--) {
        c = native_host_arm7_arm_027ead5c(p++);
        crc = native_host_arm7_arm_027eadf4(c, crc);
    }
    rcrc = ((FLASH_TABLE *)((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->pFlashImg)->checkSum;
    if (pCrc != 0 ) {
        *pCrc = (crc << 16) | rcrc;
    }
    if (crc != rcrc) {
        return 1;
    }
    return 0;
}
