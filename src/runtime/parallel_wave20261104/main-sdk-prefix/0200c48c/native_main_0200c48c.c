#include "context_00.h"
u32 native_main_0200c48c (u32 dma_no)
{
	;
	{
		OSIntrMode bak_psr = native_fn_02007ff4();
		u32 bak_dma_no = native_data_main_020e535c.field_0004;
		BOOL bak_stat = native_fn_0200bb2c(&native_data_main_020e535c.field_0018);
		native_data_main_020e535c.field_0004 = dma_no;
		if (bak_stat)
			(void)native_fn_0200bbc8(&native_data_main_020e535c.field_0018);
		(void)native_fn_02008008(bak_psr);
		return bak_dma_no;
	}
}
