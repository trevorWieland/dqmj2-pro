#include "wl_complete_types.h"
u8 native_host_arm7_main_027ead5c(void *p);
void native_host_arm7_main_027ead30(void *p,u8 data);


u32 native_host_arm7_main_027ea3b0(u16 len, u8 *pSSID)
{
    LPWORK_PARAM pWork = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work;
    u8 *pBuf, *pMask;
    u32 mask, ssid, myss;
    u32 i;
    if (len > 32 ) {
        return 0 ;
    }
    if (pWork->SSIDLength == 0) {
        return 1 ;
    }
    if (((LPWL_MAN)native_host_arm7_data_0380fff4) ->MLME.State == (0x03 | 0x10) ) {
        if (len < pWork->SSIDLength) {
            return 0 ;
        }
        len = pWork->SSIDLength;
    } else {
        if (len != pWork->SSIDLength) {
            return 0 ;
        }
    }
    pBuf = pWork->SSID;
    pMask = pWork->SSIDMask;
    for (i = 0; i < len; i++) {
        mask = native_host_arm7_main_027ead5c(pMask);
        pMask++;
        ssid = native_host_arm7_main_027ead5c(pSSID);
        pSSID++;
        myss = native_host_arm7_main_027ead5c(pBuf);
        pBuf++;
        if ((ssid | mask) != (myss | mask)) {
            return 0 ;
        }
    }
    return 1 ;
}


void native_host_arm7_main_027ead30(void *p, u8 data)
{
    { if ((u32)p & 1) *(u16 *)((u32)p - 1) = (*(u16 *)((u32)p - 1) & 0x00FF) | ( data << 8); else *(u16 *)(p) = (*(u16 *)(p) & 0xFF00) | ( data & 0x00FF); } ;
}


u8 native_host_arm7_main_027ead5c(void *p)
{
    u16 data;
    { if ((u32)p & 1) data = (u8)(*(u16 *)((u32)p - 1) >> 8); else data = (u8)(*(u16 *)(p)); } ;
    return (u8)data;
}
