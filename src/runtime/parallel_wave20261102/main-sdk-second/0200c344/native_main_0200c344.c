#include "context_00.h"
void native_main_0200c344 (u32 default_dma_no)
{
	native_data_main_020e535c.field_0004 = default_dma_no;
	native_data_main_020e535c.field_0000 = native_fn_020060e4();
	native_data_main_020e535c.field_0008.offset = 0;
	native_data_main_020e535c.field_0008.length = 0;
	native_data_main_020e535c.field_0010.offset = 0;
	native_data_main_020e535c.field_0010.length = 0;
	native_fn_02011194();
	native_fn_0200b6a8(&native_data_main_020e535c.field_0018);
	(void)native_fn_0200b714(&native_data_main_020e535c.field_0018, native_data_main_020dcb60, 3);
	if (MB_IsMultiBootChild()) {
		native_data_main_020e535c.field_0008.offset = (u32) ~0;
		native_data_main_020e535c.field_0008.length = 0;
		native_data_main_020e535c.field_0010.offset = (u32) ~0;
		native_data_main_020e535c.field_0010.length = 0;
		native_fn_0200bc38(&native_data_main_020e535c.field_0018, native_fn_0200c33c, (u32)(~0) );
		(void)native_fn_0200b84c(&native_data_main_020e535c.field_0018, 0x00000000,
		                     0, 0, 0, 0, native_fn_0200c334, native_fn_0200c2c0);
	} else {
		const CARDRomRegion *const fnt = CARD_GetRomRegionFNT();
		const CARDRomRegion *const fat = CARD_GetRomRegionFAT();
		native_fn_0200bc38(&native_data_main_020e535c.field_0018, native_fn_0200c2c8,
		                  (1 << FS_COMMAND_WRITEFILE) |
		                  (1 << FS_COMMAND_ACTIVATE) | (1 << FS_COMMAND_IDLE) );
		if ((fnt->offset == 0xFFFFFFFF) || (fnt->offset == 0x00000000) ||
		    (fat->offset == 0xFFFFFFFF) || (fat->offset == 0x00000000)) {
			((void)0) ;
		} else {
			(void)native_fn_0200b84c(&native_data_main_020e535c.field_0018, 0x00000000,
			                     fat->offset, fat->length,
			                     fnt->offset, fnt->length,
			                     native_fn_0200c278, native_fn_0200c2c0);
		}
	}
}
