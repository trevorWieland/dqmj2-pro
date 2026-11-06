#include "context_00.h"
u32 native_main_0200c4fc (const FSOverlayInfo *p_ovi)
{
	u32 size = (((p_ovi->header.flag & 0x0001 ) != 0)
	                ? p_ovi->header.compressed : p_ovi->header.ram_size);
	return size;
}
