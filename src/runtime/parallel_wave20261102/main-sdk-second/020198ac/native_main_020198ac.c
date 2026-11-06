#include "context_00.h"
void native_main_020198ac (void *arg)
{
	CTRDGiTaskWork *const p = (CTRDGiTaskWork *) arg;
	for (;;) {
		CTRDGTaskInfo trg;
		MI_CpuClear8(&trg, sizeof(CTRDGTaskInfo));
		{
			OSIntrMode bak_cpsr = native_fn_02007ff4();
			while (!p->list) {
				native_fn_020068d4(((void *)0) );
			}
			trg = *p->list;
			(void)native_fn_02008008(bak_cpsr);
		}
		if (trg.task)
			trg.result = (u32)(*trg.task)(&trg);
		{
			OSIntrMode bak_cpsr = native_fn_02007ff4();
			CTRDG_TASK_FUNC callback = trg.callback;
			native_data_main_020ec588.field_0004.busy = 0 ;
			if (callback)
				(void)(*callback)(&trg);
			if (native_data_main_020ec588.field_0000 == ((void *)0) )
				break;
			p->list = ((void *)0) ;
			(void)native_fn_02008008(bak_cpsr);
		}
	}
	((void)0) ;
	native_fn_020066ec();
	return;
}
