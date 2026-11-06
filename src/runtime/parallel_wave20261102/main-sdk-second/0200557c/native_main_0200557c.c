#include "context_00.h"
void native_main_0200557c (const void *pSrc, u32 destSlotAddr, u32 szByte)
{
	void *pLCDC;
	((void) 0) ;
	((void) 0) ;
	((void) 0) ;
	((void) 0) ;
	((void) 0) ;
	((void) 0) ;
	GX_RegionCheck_Tex(native_data_main_020e333c.field_0014, destSlotAddr, destSlotAddr + szByte);
	if (0 == native_data_main_020e333c.field_0018) {
		pLCDC = (void *)(native_data_main_020e333c.field_0004 + destSlotAddr);
	} else {
		if (destSlotAddr + szByte < native_data_main_020e333c.field_001c) {
			pLCDC = (void *)(native_data_main_020e333c.field_0004 + destSlotAddr);
		} else if (destSlotAddr >= native_data_main_020e333c.field_001c)   {
			pLCDC = (void *)(native_data_main_020e333c.field_0018 + destSlotAddr - native_data_main_020e333c.field_001c);
		} else {
			void *pLCDC2 = (void *)native_data_main_020e333c.field_0018;
			u32 sz = native_data_main_020e333c.field_001c - destSlotAddr;
			pLCDC = (void *)(native_data_main_020e333c.field_0004 + destSlotAddr);
			GXi_DmaCopy32(native_data_main_020dcb44, pSrc, pLCDC, sz);
			GXi_DmaCopy32Async(native_data_main_020dcb44, (void *)((u8 *)pSrc + sz), pLCDC2, szByte - sz, ((void *)0) , ((void *)0) );
			return;
		}
	}
	GXi_DmaCopy32Async(native_data_main_020dcb44, pSrc, pLCDC, szByte, ((void *)0) , ((void *)0) );
}
