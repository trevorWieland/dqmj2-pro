#include "context_00.h"
void native_main_02018c14 (void * p_work, u32 size)
{
	OSIntrMode bak_cpsr = native_fn_02007ff4();
	if (!native_data_main_020ec3a0.field_0000) {
		MBiTaskWork * const p = (MBiTaskWork *) p_work;
		((void) 0) ;
		((void) 0) ;
		native_data_main_020ec3a0.field_0000 = p;
		native_fn_02018cb0(&p->end_task);
		p->list = ((void *)0) ;
		size = (u32)((size - sizeof(MBiTaskWork)) & ~3);
		native_fn_020065f0(p->th, native_fn_02018afc, p, (u8 *)(p + 1) + size, size, 0 );
		native_fn_0200698c(p->th);
	}
	(void)native_fn_02008008(bak_cpsr);
}
