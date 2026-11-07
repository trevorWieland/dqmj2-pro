#include "context000.h"

#include "context001.h"

void native_host_arm7_main_027eb13c(void)
{
    ;
    ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Config.DiagResult |= 0x8000;
    if (((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Work.STA != 0x00 ) {
        native_host_arm7_arm_037f9198();
        if (((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->MLME.State != 0x00 ) {
            ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->MLME.State = 0x00 ;
            ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->MLME.pCfm.Cfm->resultCode = 0x06 ;
            native_host_arm7_arm_027edb20();
        }
        native_host_arm7_arm_027e9d00();
    }
    while (native_host_arm7_arm_037f8650(3 ) != 0xFFFF ) {}
    native_host_arm7_arm_037f8598(3 , 23 );
}
