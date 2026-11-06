#include "context_00.h"
void native_main_020051f8 (const void *pSrc, u32 destSlotAddr, u32 szByte)
{
	((void) 0) ;
	((void) 0) ;
	((void) 0) ;
	((void) 0) ;
	((void) 0) ;
	((void) 0) ;
	GXi_DmaCopy32Async(native_data_main_020dcb44,
	                   pSrc,
	                   (void *)(native_data_main_020e3320.field_0010 + destSlotAddr - native_data_main_020e3320.field_000c),
	                   szByte, ((void *)0) , ((void *)0) );
}
