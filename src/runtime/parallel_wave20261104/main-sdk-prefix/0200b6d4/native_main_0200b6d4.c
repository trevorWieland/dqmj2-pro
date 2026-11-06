#include "context_00.h"
FSArchive *native_main_0200b6d4 (const char *name, int name_len)
{
	u32 pack = native_fn_0200b16c(name, name_len);
	OSIntrMode bak_psr = native_fn_02007ff4();
	FSArchive *p_arc = native_data_main_020e5348.field_0000;
	while (p_arc && (p_arc->name.pack != pack))
		p_arc = p_arc->next;
	(void)native_fn_02008008(bak_psr);
	return p_arc;
}
