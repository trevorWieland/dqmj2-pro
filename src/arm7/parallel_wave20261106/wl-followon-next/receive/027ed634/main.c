#include "context000.h"

#include "context001.h"

void native_host_arm7_main_027ed634(void *arg)
{
    LPMLME_MAN pMLME = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->MLME;
    pMLME->pCfm.Auth->resultCode = 0x07 ;
    pMLME->State = (0x05 | 0x30) ;
    native_host_arm7_arm_037f8598(2 , 2 );
}
