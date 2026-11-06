#include "context_00.h"
FSResult native_main_0200c278 (FSArchive *p_arc, void *dst, u32 src, u32 len)
{
	CARD_ReadRomAsync(native_data_main_020e535c.field_0004, (const void *)src, dst, len, native_fn_0200c254, p_arc);
	return FS_RESULT_PROC_ASYNC;
}
