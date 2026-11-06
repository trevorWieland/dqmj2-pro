#include "context_00.h"
void native_main_02018cdc (MBiTaskInfo * pt, MB_TASK_FUNC task, MB_TASK_FUNC callback, u32 priority)
{
	MBiTaskWork * const p_work = native_data_main_020ec3a0.field_0000;
	((void) 0) ;
	if (!native_fn_02018c94()) {
		((void)0) ;
		return;
	}
	if (pt->busy) {
		((void)0) ;
		return;
	}
	if (priority > 31 ) {
		const u32 cur_priority = native_fn_02006b74(p_work->th);
		if (priority == (31 + 1) ) {
			priority = (u32)((cur_priority > 0 ) ? (cur_priority - 1) : 0 );
		} else if (priority == (31 + 2) )   {
			priority = (u32)((cur_priority < 31 ) ? (cur_priority + 1) : 31 );
		} else if (priority == (31 + 3) )   {
			priority = cur_priority;
		} else {
			priority = 31 ;
		}
	}
	{
		OSIntrMode bak_cpsr = native_fn_02007ff4();
		pt->busy = 1 ;
		pt->priority = priority;
		pt->task = task;
		pt->callback = callback;
		if (!p_work->list) {
			if (pt == &p_work->end_task) {
				native_data_main_020ec3a0.field_0000 = ((void *)0) ;
			}
			p_work->list = pt;
			native_fn_0200698c(p_work->th);
		} else {
			MBiTaskInfo * pos = p_work->list;
			if (pt == &p_work->end_task) {
				while (pos->next)
					pos = pos->next;
				pos->next = pt;
				native_data_main_020ec3a0.field_0000 = ((void *)0) ;
			} else {
				if (pos->priority > priority) {
					p_work->list = pt;
					pt->next = pos;
				} else {
					while (pos->next && (pos->next->priority <= priority))
						pos = pos->next;
					pt->next = pos->next;
					pos->next = pt;
				}
			}
		}
		(void)native_fn_02008008(bak_cpsr);
	}
}
