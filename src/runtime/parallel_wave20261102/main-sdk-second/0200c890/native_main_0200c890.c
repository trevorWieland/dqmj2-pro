#include "context_00.h"
void native_main_0200c890 (FSOverlayInfo *p_ovi)
{
	u32 rare_size = native_fn_0200c4fc(p_ovi);
	if (MB_IsMultiBootChild()) {
		BOOL ret = 0 ;
		if ((p_ovi->header.flag & 0x0002 ) != 0) {
			const u32 odt_max =
				(u32)((native_data_main_020e3300 - native_data_main_020e3300) / (160 / 8) );
			if (p_ovi->header.id < odt_max) {
				const u8 *spec_digest = (native_data_main_020e3300 +
				                         (160 / 8) * p_ovi->header.id);
				ret = native_fn_0200c7fc(spec_digest, p_ovi->header.ram_address, (int)rare_size);
			}
		}
		if (!ret) {
			MI_CpuClear8(p_ovi->header.ram_address, rare_size);
			native_fn_02008430() ;
			return;
		}
	}
	if ((p_ovi->header.flag & 0x0001 ) != 0) {
		native_fn_02000950(p_ovi->header.ram_address + rare_size);
	}
	native_fn_02007308(FS_GetOverlayAddress(p_ovi), FS_GetOverlayImageSize(p_ovi));
	{
		FSOverlayInitFunc *p = p_ovi->header.sinit_init;
		FSOverlayInitFunc *q = p_ovi->header.sinit_init_end;
		for (; p < q; ++p) {
			if (*p)
				(**p)();
		}
	}
}
