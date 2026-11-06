#include "context_00.h"
BOOL native_main_0200c7fc (const u8 *spec_digest, void *src, int len)
{
	int i;
	u8 digest[(160 / 8) ];
	u8 digest_key[64];
	MI_CpuClear8(digest, sizeof(digest));
	native_fn_02008e0c(native_data_main_020dcb64.field_0000, digest_key, (u32)native_data_main_020dcb64.field_0004);
	native_fn_0200d3e4(digest, src, len, digest_key, native_data_main_020dcb64.field_0004);
	for (i = 0; i < sizeof(digest); i += sizeof(u32)) {
		if (*(const u32 *)(digest + i) != *(const u32 *)(spec_digest + i))
			break;
	}
	return (i == sizeof(digest));
}
