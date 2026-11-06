#include "../20261101_wl_counter504/wl_complete_types.h"
extern void native_host_arm7_wram_037fdfd0(u32 data,void *destination,u32 size);
static inline void MI_CpuFill32 (void * dest, u32 data, u32 size)
{
	native_host_arm7_wram_037fdfd0(data, dest, size);
}
static inline void MI_CpuClear32 (void * dest, u32 size)
{
	MI_CpuFill32(dest, 0, size);
}
void native_host_arm7_wram_037fb1e0(void)
{
    LPWORK_PARAM pWork = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work;
    LPRX_CTRL pRxCtrl = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->RxCtrl;
    u32 str_madrs;
    MI_CpuClear32((void *)(u32)pRxCtrl, sizeof(RX_CTRL)) ;
    *(u16 *)((0x04808000) + 0x030) = 0x8000;
    switch (((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work.Mode) {
    case 0 :
        str_madrs = (((0x0000 + ((8 + 12 + 24) - 6 + 2)) + (((8 + 12 + 24) + 8 + 12) + 261 + 3)) + (((8 + 12 + 24) + 8 + 12) + 1508 + 0)) ;
        break;
    case 1 :
        str_madrs = (((((0x0000 + ((8 + 12 + 24) + 2 + 2 + 2 + 516 + 2)) + ((8 + 12 + 24) + 208 + 0)) + (((8 + 12 + 24) + 8 + 12) + 1508 + 0)) + (((8 + 12 + 24) + 8 + 12) + 261 + 3)) + (((8 + 12 + 24) + 8 + 12) + 1508 + 0)) ;
        break;
    case 2 :
        str_madrs = (((((0x0000 + ((8 + 12 + 24) + 2 + 516 + 2)) + ((8 + 12 + 24) + 2 + 516 + 2)) + ((8 + 12 + 24) - 6 + 2)) + (((8 + 12 + 24) + 8 + 12) + 261 + 3)) + (((8 + 12 + 24) + 8 + 12) + 1508 + 0)) ;
        break;
    case 3 :
        str_madrs = (((0x0000 + ((8 + 12 + 24) - 6 + 2)) + (((8 + 12 + 24) + 8 + 12) + 261 + 3)) + (((8 + 12 + 24) + 8 + 12) + 1508 + 0)) ;
        break;
    }
    *(vu16 *)(0x04808000 + 0x050) = (u16)((0x04800000 + 0x4000) + str_madrs);
    *(vu16 *)((0x04808000) + 0x056) = str_madrs / 2;
    *(vu16 *)(0x04808000 + 0x052) = (u16)((0x04800000 + 0x4000) + 0x1F60 );
    *(vu16 *)((0x04808000) + 0x05A) = str_madrs / 2;
    pRxCtrl->wlCurr = str_madrs / 2;
    pRxCtrl->LastMpSeq = 0xFFFF;
    pWork->Ofst.RxBuf.Size = 0x1F60 - str_madrs;
    *(vu16 *)(0x04808000 + 0x062) = (u16)((0x04800000 + 0x4000) + 0x1F60 - 2);
    *(u16 *)((0x04808000) + 0x030) = 0x8001;
    *(u16 *)((0x04808000) + 0x24C) = 0xFFFF;
    *(u16 *)((0x04808000) + 0x24C + 2) = 0xFFFF;
    *(u16 *)((0x04800000 + 0x4000) + 0x1f70) = 0xFFFF;
    *(u16 *)((0x04800000 + 0x4000) + 0x1f72) = 0xFFFF;
    *(vu16 *)((0x04800000 + 0x4000) + 0x1f7e) = 0xFFFF;
    *(vu16 *)((0x04800000 + 0x4000) + 0x1f76) = 0xFFFF;
}
