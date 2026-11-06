typedef unsigned char u8;
typedef unsigned short int u16;
typedef volatile u8 vu8;
typedef volatile u16 vu16;
typedef vu8 REGType8v;
void native_fn_020082d8(u16 bank, u16 lockId);
typedef enum {
	GX_VRAM_A = 0x0001 ,
	GX_VRAM_B = 0x0002 ,
	GX_VRAM_C = 0x0004 ,
	GX_VRAM_D = 0x0008 ,
	GX_VRAM_E = 0x0010 ,
	GX_VRAM_F = 0x0020 ,
	GX_VRAM_G = 0x0040 ,
	GX_VRAM_H = 0x0080 ,
	GX_VRAM_I = 0x0100 ,
	GX_VRAM_ALL = 0x01ff
} GXVRam;
typedef enum {
	GX_VRAM_LCDC_NONE = 0x0000,
	GX_VRAM_LCDC_A = GX_VRAM_A,
	GX_VRAM_LCDC_B = GX_VRAM_B,
	GX_VRAM_LCDC_C = GX_VRAM_C,
	GX_VRAM_LCDC_D = GX_VRAM_D,
	GX_VRAM_LCDC_E = GX_VRAM_E,
	GX_VRAM_LCDC_F = GX_VRAM_F,
	GX_VRAM_LCDC_G = GX_VRAM_G,
	GX_VRAM_LCDC_H = GX_VRAM_H,
	GX_VRAM_LCDC_I = GX_VRAM_I,
	GX_VRAM_LCDC_ALL = GX_VRAM_ALL
} GXVRamLCDC;
extern vu16 native_data_main_020e3302;
int native_main_02003c18 (u16 *g3bit)
{
	int rval = *g3bit;
	*g3bit = 0;
	if (rval & GX_VRAM_LCDC_A)
		(*( REGType8v *) (0x04000000 + 0x240)) = 0;
	if (rval & GX_VRAM_LCDC_B)
		(*( REGType8v *) (0x04000000 + 0x241)) = 0;
	if (rval & GX_VRAM_LCDC_C)
		(*( REGType8v *) (0x04000000 + 0x242)) = 0;
	if (rval & GX_VRAM_LCDC_D)
		(*( REGType8v *) (0x04000000 + 0x243)) = 0;
	if (rval & GX_VRAM_LCDC_E)
		(*( REGType8v *) (0x04000000 + 0x244)) = 0;
	if (rval & GX_VRAM_LCDC_F)
		(*( REGType8v *) (0x04000000 + 0x245)) = 0;
	if (rval & GX_VRAM_LCDC_G)
		(*( REGType8v *) (0x04000000 + 0x246)) = 0;
	if (rval & GX_VRAM_LCDC_H)
		(*( REGType8v *) (0x04000000 + 0x248)) = 0;
	if (rval & GX_VRAM_LCDC_I)
		(*( REGType8v *) (0x04000000 + 0x249)) = 0;
	native_fn_020082d8((u16)rval, native_data_main_020e3302);
	return rval;
}
