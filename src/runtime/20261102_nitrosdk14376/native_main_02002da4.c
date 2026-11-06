typedef unsigned char u8;
typedef volatile u8 vu8;
typedef vu8 REGType8v;
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
typedef enum {
	GX_VRAMCNT_A_DISABLE           = 0,
	GX_VRAMCNT_A_LCDC_0x06800000   = (0 << 0 ) | (0 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_A_BG_0x06000000     = (1 << 0 ) | (0 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_A_BG_0x06020000     = (1 << 0 ) | (1 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_A_BG_0x06040000     = (1 << 0 ) | (2 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_A_BG_0x06060000     = (1 << 0 ) | (3 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_A_OBJ_0x06400000    = (2 << 0 ) | (0 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_A_OBJ_0x06420000    = (2 << 0 ) | (1 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_A_TEX_0             = (3 << 0 ) | (0 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_A_TEX_1             = (3 << 0 ) | (1 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_A_TEX_2             = (3 << 0 ) | (2 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_A_TEX_3             = (3 << 0 ) | (3 << 3 ) | (1 << 7 )
} GX_VRAMCNT_A;
typedef enum {
	GX_VRAMCNT_B_DISABLE           = 0,
	GX_VRAMCNT_B_LCDC_0x06820000   = (0 << 0 ) | (0 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_B_BG_0x06000000     = (1 << 0 ) | (0 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_B_BG_0x06020000     = (1 << 0 ) | (1 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_B_BG_0x06040000     = (1 << 0 ) | (2 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_B_BG_0x06060000     = (1 << 0 ) | (3 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_B_OBJ_0x06400000    = (2 << 0 ) | (0 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_B_OBJ_0x06420000    = (2 << 0 ) | (1 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_B_TEX_0             = (3 << 0 ) | (0 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_B_TEX_1             = (3 << 0 ) | (1 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_B_TEX_2             = (3 << 0 ) | (2 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_B_TEX_3             = (3 << 0 ) | (3 << 3 ) | (1 << 7 )
} GX_VRAMCNT_B;
typedef enum {
	GX_VRAMCNT_C_DISABLE           = 0,
	GX_VRAMCNT_C_LCDC_0x06840000   = (0 << 0 ) | (0 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_C_BG_0x06000000     = (1 << 0 ) | (0 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_C_BG_0x06020000     = (1 << 0 ) | (1 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_C_BG_0x06040000     = (1 << 0 ) | (2 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_C_BG_0x06060000     = (1 << 0 ) | (3 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_C_ARM7_0x06000000   = (2 << 0 ) | (0 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_C_ARM7_0x06020000   = (2 << 0 ) | (1 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_C_TEX_0             = (3 << 0 ) | (0 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_C_TEX_1             = (3 << 0 ) | (1 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_C_TEX_2             = (3 << 0 ) | (2 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_C_TEX_3             = (3 << 0 ) | (3 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_C_SUBBG_0x06200000  = (4 << 0 ) | (1 << 7 )
} GX_VRAMCNT_C;
typedef enum {
	GX_VRAMCNT_D_DISABLE           = 0,
	GX_VRAMCNT_D_LCDC_0x06860000   = (0 << 0 ) | (0 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_D_BG_0x06000000     = (1 << 0 ) | (0 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_D_BG_0x06020000     = (1 << 0 ) | (1 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_D_BG_0x06040000     = (1 << 0 ) | (2 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_D_BG_0x06060000     = (1 << 0 ) | (3 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_D_ARM7_0x06000000   = (2 << 0 ) | (0 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_D_ARM7_0x06020000   = (2 << 0 ) | (1 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_D_TEX_0             = (3 << 0 ) | (0 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_D_TEX_1             = (3 << 0 ) | (1 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_D_TEX_2             = (3 << 0 ) | (2 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_D_TEX_3             = (3 << 0 ) | (3 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_D_SUBOBJ_0x06600000 = (4 << 0 ) | (1 << 7 )
} GX_VRAMCNT_D;
typedef enum {
	GX_VRAMCNT_E_DISABLE           = 0,
	GX_VRAMCNT_E_LCDC_0x06880000   = (0 << 0 ) | (1 << 7 ),
	GX_VRAMCNT_E_BG_0x06000000     = (1 << 0 ) | (1 << 7 ),
	GX_VRAMCNT_E_OBJ_0x06400000    = (2 << 0 ) | (1 << 7 ),
	GX_VRAMCNT_E_TEXPLTT_0123      = (3 << 0 ) | (1 << 7 ),
	GX_VRAMCNT_E_BGEXTPLTT_0123    = (4 << 0 ) | (1 << 7 )
}
GX_VRAMCNT_E;
typedef enum {
	GX_VRAMCNT_F_DISABLE           = 0,
	GX_VRAMCNT_F_LCDC_0x06890000   = (0 << 0 ) | (0 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_F_BG_0x06000000     = (1 << 0 ) | (0 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_F_BG_0x06004000     = (1 << 0 ) | (1 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_F_BG_0x06010000     = (1 << 0 ) | (2 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_F_BG_0x06014000     = (1 << 0 ) | (3 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_F_OBJ_0x06400000    = (2 << 0 ) | (0 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_F_OBJ_0x06404000    = (2 << 0 ) | (1 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_F_OBJ_0x06410000    = (2 << 0 ) | (2 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_F_OBJ_0x06414000    = (2 << 0 ) | (3 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_F_TEXPLTT_0         = (3 << 0 ) | (0 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_F_TEXPLTT_1         = (3 << 0 ) | (1 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_F_TEXPLTT_4         = (3 << 0 ) | (2 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_F_TEXPLTT_5         = (3 << 0 ) | (3 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_F_BGEXTPLTT_01      = (4 << 0 ) | (0 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_F_BGEXTPLTT_23      = (4 << 0 ) | (1 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_F_OBJEXTPLTT        = (5 << 0 ) | (0 << 3 ) | (1 << 7 )
} GX_VRAMCNT_F;
typedef enum {
	GX_VRAMCNT_G_DISABLE           = 0,
	GX_VRAMCNT_G_LCDC_0x06894000   = (0 << 0 ) | (0 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_G_BG_0x06000000     = (1 << 0 ) | (0 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_G_BG_0x06004000     = (1 << 0 ) | (1 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_G_BG_0x06010000     = (1 << 0 ) | (2 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_G_BG_0x06014000     = (1 << 0 ) | (3 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_G_OBJ_0x06400000    = (2 << 0 ) | (0 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_G_OBJ_0x06404000    = (2 << 0 ) | (1 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_G_OBJ_0x06410000    = (2 << 0 ) | (2 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_G_OBJ_0x06414000    = (2 << 0 ) | (3 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_G_TEXPLTT_0         = (3 << 0 ) | (0 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_G_TEXPLTT_1         = (3 << 0 ) | (1 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_G_TEXPLTT_4         = (3 << 0 ) | (2 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_G_TEXPLTT_5         = (3 << 0 ) | (3 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_G_BGEXTPLTT_01      = (4 << 0 ) | (0 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_G_BGEXTPLTT_23      = (4 << 0 ) | (1 << 3 ) | (1 << 7 ),
	GX_VRAMCNT_G_OBJEXTPLTT        = (5 << 0 ) | (0 << 3 ) | (1 << 7 )
} GX_VRAMCNT_G;
typedef enum {
	GX_VRAMCNT_H_DISABLE           = 0,
	GX_VRAMCNT_H_LCDC_0x06898000   = (0 << 0 ) | (1 << 7 ),
	GX_VRAMCNT_H_SUBBG_0x06200000  = (1 << 0 ) | (1 << 7 ),
	GX_VRAMCNT_H_SUBBGEXTPLTT_0123 = (2 << 0 ) | (1 << 7 )
} GX_VRAMCNT_H;
typedef enum {
	GX_VRAMCNT_I_DISABLE           = 0,
	GX_VRAMCNT_I_LCDC_0x068A0000   = (0 << 0 ) | (1 << 7 ),
	GX_VRAMCNT_I_SUBBG_0x06208000  = (1 << 0 ) | (1 << 7 ),
	GX_VRAMCNT_I_SUBOBJ_0x06600000 = (2 << 0 ) | (1 << 7 ),
	GX_VRAMCNT_I_SUBOBJEXTPLTT     = (3 << 0 ) | (1 << 7 )
} GX_VRAMCNT_I;
void native_main_02002da4 (int lcdc)
{
	if (lcdc & GX_VRAM_LCDC_A)
		(*( REGType8v *) (0x04000000 + 0x240)) = (u8)GX_VRAMCNT_A_LCDC_0x06800000;
	if (lcdc & GX_VRAM_LCDC_B)
		(*( REGType8v *) (0x04000000 + 0x241)) = (u8)GX_VRAMCNT_B_LCDC_0x06820000;
	if (lcdc & GX_VRAM_LCDC_C)
		(*( REGType8v *) (0x04000000 + 0x242)) = (u8)GX_VRAMCNT_C_LCDC_0x06840000;
	if (lcdc & GX_VRAM_LCDC_D)
		(*( REGType8v *) (0x04000000 + 0x243)) = (u8)GX_VRAMCNT_D_LCDC_0x06860000;
	if (lcdc & GX_VRAM_LCDC_E)
		(*( REGType8v *) (0x04000000 + 0x244)) = (u8)GX_VRAMCNT_E_LCDC_0x06880000;
	if (lcdc & GX_VRAM_LCDC_F)
		(*( REGType8v *) (0x04000000 + 0x245)) = (u8)GX_VRAMCNT_F_LCDC_0x06890000;
	if (lcdc & GX_VRAM_LCDC_G)
		(*( REGType8v *) (0x04000000 + 0x246)) = (u8)GX_VRAMCNT_G_LCDC_0x06894000;
	if (lcdc & GX_VRAM_LCDC_H)
		(*( REGType8v *) (0x04000000 + 0x248)) = (u8)GX_VRAMCNT_H_LCDC_0x06898000;
	if (lcdc & GX_VRAM_LCDC_I)
		(*( REGType8v *) (0x04000000 + 0x249)) = (u8)GX_VRAMCNT_I_LCDC_0x068A0000;
}
