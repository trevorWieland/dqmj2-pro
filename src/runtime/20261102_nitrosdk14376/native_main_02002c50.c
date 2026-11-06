typedef unsigned short int u16;
typedef unsigned long u32;
typedef volatile u32 vu32;
typedef vu32 REGType32v;
typedef enum {
	GX_DISPMODE_GRAPHICS = 0x01,
	GX_DISPMODE_VRAM_A = 0x02,
	GX_DISPMODE_VRAM_B = 0x06,
	GX_DISPMODE_VRAM_C = 0x0a,
	GX_DISPMODE_VRAM_D = 0x0e,
	GX_DISPMODE_MMEM = 0x03
} GXDispMode;
void native_main_02002c50(void);
extern u16 native_data_main_020e3300;
extern u16 native_data_main_020dcb40;
void native_main_02002c50 (void)
{
	native_data_main_020dcb40 = 1 ;
	if (native_data_main_020e3300 != (u16)((GXDispMode)0x00) ) {
		(*( REGType32v *) (0x04000000 + 0x000)) =
			(((*( REGType32v *) (0x04000000 + 0x000)) & ~0x00030000 ) |
			 (native_data_main_020e3300 << 16 ));
	} else {
		(*( REGType32v *) (0x04000000 + 0x000)) = (((*( REGType32v *) (0x04000000 + 0x000)) | (GX_DISPMODE_GRAPHICS << 16 )));
	}
}
