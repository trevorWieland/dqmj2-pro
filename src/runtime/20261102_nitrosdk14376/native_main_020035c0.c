typedef unsigned char u8;
typedef unsigned short int u16;
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
	GX_VRAM_TEXPLTT_NONE          = 0x0000,
	GX_VRAM_TEXPLTT_0_F           = GX_VRAM_F,
	GX_VRAM_TEXPLTT_0_G           = GX_VRAM_G,
	GX_VRAM_TEXPLTT_01_FG         = GX_VRAM_F | GX_VRAM_G,
	GX_VRAM_TEXPLTT_0123_E        = GX_VRAM_E,
	GX_VRAM_TEXPLTT_01234_EF      = GX_VRAM_E | GX_VRAM_F,
	GX_VRAM_TEXPLTT_012345_EFG    = GX_VRAM_E | GX_VRAM_F | GX_VRAM_G
} GXVRamTexPltt;
    void native_main_020035c0(GXVRamTexPltt texPltt);
typedef struct {
	u16 lcdc;
	u16 bg;
	u16 obj;
	u16 arm7;
	u16 tex;
	u16 texPltt;
	u16 clrImg;
	u16 bgExtPltt;
	u16 objExtPltt;
	u16 sub_bg;
	u16 sub_obj;
	u16 sub_bgExtPltt;
	u16 sub_objExtPltt;
} GX_VRAMCnt_;
typedef struct {
	GX_VRAMCnt_ vramCnt;
} GX_State;
extern GX_State native_data_main_020e3304;
    static inline void GX_StateCheck_VRAMCnt (void)
    {
    }
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
void native_fn_02002da4 (int lcdc);
static inline void GX_VRAMCNT_SetTEXPLTT_ (GXVRamTexPltt texPltt)
{
	switch (texPltt) {
	case GX_VRAM_TEXPLTT_01_FG:
		(*( REGType8v *) (0x04000000 + 0x246)) = (u8)GX_VRAMCNT_G_TEXPLTT_1;
	case GX_VRAM_TEXPLTT_0_F:
		(*( REGType8v *) (0x04000000 + 0x245)) = (u8)GX_VRAMCNT_F_TEXPLTT_0;
		break;
	case GX_VRAM_TEXPLTT_0_G:
		(*( REGType8v *) (0x04000000 + 0x246)) = (u8)GX_VRAMCNT_G_TEXPLTT_0;
		break;
	case GX_VRAM_TEXPLTT_012345_EFG:
		(*( REGType8v *) (0x04000000 + 0x246)) = (u8)GX_VRAMCNT_G_TEXPLTT_5;
	case GX_VRAM_TEXPLTT_01234_EF:
		(*( REGType8v *) (0x04000000 + 0x245)) = (u8)GX_VRAMCNT_F_TEXPLTT_4;
	case GX_VRAM_TEXPLTT_0123_E:
		(*( REGType8v *) (0x04000000 + 0x244)) = (u8)GX_VRAMCNT_E_TEXPLTT_0123;
		break;
	case GX_VRAM_TEXPLTT_NONE:
		break;
	default:
		((void) 0) ;
		break;
	}
}
static inline void GxSetBankForTexPltt (GXVRamTexPltt texPltt)
{
	((void) 0) ;
	native_data_main_020e3304.vramCnt.lcdc = (u16)(~texPltt & (native_data_main_020e3304.vramCnt.lcdc | native_data_main_020e3304.vramCnt.texPltt));
	native_data_main_020e3304.vramCnt.texPltt = texPltt;
	GX_StateCheck_VRAMCnt();
	GX_VRAMCNT_SetTEXPLTT_(texPltt);
	native_fn_02002da4(native_data_main_020e3304.vramCnt.lcdc);
}
void native_main_020035c0 (GXVRamTexPltt texPltt)
{
	GxSetBankForTexPltt(texPltt);
}
