#include "context_00.h"
void native_main_0200573c (const void *pSrc, u32 destSlotAddr, u32 szByte)
{
	((void) 0) ;
	((void) 0) ;
	((void) 0) ;
	((void) 0) ;
	((void) 0) ;
	((void) 0) ;
	GX_RegionCheck_TexPltt(native_data_main_020e333c.field_000c, destSlotAddr, destSlotAddr + szByte);
	GXi_DmaCopy32Async(native_data_main_020dcb44, pSrc, (void *)(native_data_main_020e333c.field_0008 + destSlotAddr), szByte, ((void *)0) , ((void *)0) );
}
