#include "context000.h"

#include "context001.h"

void native_host_arm7_main_027ea048(void)
{
    LPWORK_PARAM pWork = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Work;
    pWork->AID = 0;
    native_host_arm7_arm_037fb3b4();
    *(vu16 *)((0x04808000) + 0x02A) = 0;
    if (pWork->APCamAdrs != 0) {
        native_host_arm7_arm_027f0d6c(pWork->APCamAdrs);
        native_host_arm7_arm_027ebc50(pWork->APCamAdrs, 0x20 );
        pWork->APCamAdrs = 0;
    }
}
