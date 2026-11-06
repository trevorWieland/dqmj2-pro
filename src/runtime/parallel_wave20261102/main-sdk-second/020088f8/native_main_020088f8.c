#include "context_00.h"
void native_main_020088f8 (u32 dmaNo, const void * src, u32 commandLength, MIDmaCallback callback, void * arg)
{
	((void) 0) ;
	((void) 0) ;
	((void)0) ;
	if (commandLength == 0) {
		MIi_CallCallback(callback, arg);
		return;
	}
	while (native_data_main_020e3740.field_0000.isBusy  ) {
	}
	while (!(G3X_GetCommandFifoStatus() & GX_FIFOSTAT_UNDERHALF)) {
	}
	native_data_main_020e3740.field_0000.isBusy = 1 ;
	native_data_main_020e3740.field_0000.dmaNo = dmaNo;
	native_data_main_020e3740.field_0000.src = (u32)src;
	native_data_main_020e3740.field_0000.length = commandLength;
	native_data_main_020e3740.field_0000.callback = callback;
	native_data_main_020e3740.field_0000.arg = arg;
	native_fn_020088a4(dmaNo, (u32)src, commandLength, (0UL << 23) );
	native_fn_02008714(dmaNo);
	{
		OSIntrMode enabled = native_fn_02007ff4();
		native_data_main_020e3740.field_0000.fifoCond = (GXFifoIntrCond)(((*( REGType32v *) (0x04000000 + 0x600)) & 0xc0000000 ) >> 30 );
		native_data_main_020e3740.field_0000.fifoFunc = native_fn_02005bd8((1UL << 21) );
		G3X_SetFifoIntrCond(GX_FIFOINTR_COND_UNDERHALF);
		native_fn_02005b50((1UL << 21) , native_fn_020089f0);
		(void)native_fn_02005d20((1UL << 21) );
		native_fn_020089f0();
		(void)native_fn_02008008(enabled);
	}
}
