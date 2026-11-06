#include "context_00.h"
void native_main_02002a94 (void)
{
	const u16 bg_mtx_elem_one = 1 << 8;
	(*( REGType16v *) (0x04000000 + 0x304)) |= (1 << 15 );
	GX_SetPower(GX_POWER_ALL);
	GXi_PowerLCD(1 );
	native_fn_02002d44();
	{
		s32 lockResult;
		while (native_data_main_020e3300.field_0002 == 0) {
			lockResult = native_fn_020060e4();
			if (lockResult == (-3) ) {
				native_fn_02008430() ;
			}
			native_data_main_020e3300.field_0002 = (u16)lockResult;
		}
	}
	(*( REGType16v *) (0x04000000 + 0x004)) = 0;
	(*( REGType32v *) (0x04000000 + 0x000)) = 0;
	if (native_data_main_020dcb40.field_0004 != ((u32) ~0) ) {
		native_fn_0200845c(native_data_main_020dcb40.field_0004, (void *)(0x04000000 + 0x008) , 0,
		             (0x04000000 + 0x068) - (0x04000000 + 0x008) );
		(*( REGType16v *) (0x04000000 + 0x06c)) = 0;
		native_fn_0200845c(native_data_main_020dcb40.field_0004, (void *)(0x04000000 + 0x1000) , 0,
		             (0x04000000 + 0x106c) - (0x04000000 + 0x1000) + 4);
	} else {
		MI_CpuFill32((void *)(0x04000000 + 0x008) , 0, (0x04000000 + 0x068) - (0x04000000 + 0x008) );
		(*( REGType16v *) (0x04000000 + 0x06c)) = 0;
		MI_CpuFill32((void *)(0x04000000 + 0x1000) , 0,
		             (0x04000000 + 0x106c) - (0x04000000 + 0x1000) + 4);
	}
	(*( REGType16v *) (0x04000000 + 0x020)) = bg_mtx_elem_one;
	(*( REGType16v *) (0x04000000 + 0x026)) = bg_mtx_elem_one;
	(*( REGType16v *) (0x04000000 + 0x030)) = bg_mtx_elem_one;
	(*( REGType16v *) (0x04000000 + 0x036)) = bg_mtx_elem_one;
	(*( REGType16v *) (0x04000000 + 0x1020)) = bg_mtx_elem_one;
	(*( REGType16v *) (0x04000000 + 0x1026)) = bg_mtx_elem_one;
	(*( REGType16v *) (0x04000000 + 0x1030)) = bg_mtx_elem_one;
	(*( REGType16v *) (0x04000000 + 0x1036)) = bg_mtx_elem_one;
}
