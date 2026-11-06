#include "context_00.h"
void native_main_0201109c (u32 dma,
                    const void *src, void *dst, u32 len,
                    MIDmaCallback callback, void *arg, BOOL is_async)
{
	CARDRomStat *const p = &native_data_main_020e5b20.field_0020;
	CARDiCommon *const c = &native_data_main_020e5500;
	((void) 0) ;
	((void) 0) ;
	((void) 0) ;
	native_fn_02010204();
	CARDi_WaitTask(c, callback, arg);
	c->dma = dma;
	c->src = (u32)((u32)src + native_data_main_020e5b20.field_0000);
	c->dst = (u32)dst;
	c->len = (u32)len;
	if (dma <= 3 )
		native_fn_0200877c(dma);
	if (native_fn_02010d2c(p)) {
		if (!is_async)
			native_fn_020111f8();
	} else if (is_async)   {
		native_fn_0200ff98(native_fn_02011004);
	} else {
		c->cur_th = OS_GetCurrentThread();
		native_fn_02011004(c);
	}
}
