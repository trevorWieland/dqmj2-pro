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
	GX_VRAM_SUB_OBJ_NONE     = 0x0000,
	GX_VRAM_SUB_OBJ_128_D    = GX_VRAM_D,
	GX_VRAM_SUB_OBJ_16_I     = GX_VRAM_I
} GXVRamSubOBJ;
    void native_main_02003950(GXVRamSubOBJ sub_obj);
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
	GX_VRAMCNT_I_DISABLE           = 0,
	GX_VRAMCNT_I_LCDC_0x068A0000   = (0 << 0 ) | (1 << 7 ),
	GX_VRAMCNT_I_SUBBG_0x06208000  = (1 << 0 ) | (1 << 7 ),
	GX_VRAMCNT_I_SUBOBJ_0x06600000 = (2 << 0 ) | (1 << 7 ),
	GX_VRAMCNT_I_SUBOBJEXTPLTT     = (3 << 0 ) | (1 << 7 )
} GX_VRAMCNT_I;
void native_fn_02002da4 (int lcdc);
static inline void GX_VRAMCNT_SetSubOBJ_ (GXVRamSubOBJ obj)
{
	switch (obj) {
	case GX_VRAM_SUB_OBJ_128_D:
		(*( REGType8v *) (0x04000000 + 0x243)) = GX_VRAMCNT_D_SUBOBJ_0x06600000;
		break;
	case GX_VRAM_SUB_OBJ_16_I:
		(*( REGType8v *) (0x04000000 + 0x249)) = GX_VRAMCNT_I_SUBOBJ_0x06600000;
		break;
	case GX_VRAM_SUB_OBJ_NONE:
		break;
	default:
		((void) 0) ;
		break;
	}
}
static inline void GxSetBankForSubOBJ (GXVRamSubOBJ sub_obj)
{
	((void) 0) ;
	native_data_main_020e3304.vramCnt.lcdc = (u16)(~sub_obj & (native_data_main_020e3304.vramCnt.lcdc | native_data_main_020e3304.vramCnt.sub_obj));
	native_data_main_020e3304.vramCnt.sub_obj = sub_obj;
	GX_StateCheck_VRAMCnt();
	GX_VRAMCNT_SetSubOBJ_(sub_obj);
	native_fn_02002da4(native_data_main_020e3304.vramCnt.lcdc);
}
void native_main_02003950 (GXVRamSubOBJ sub_obj)
{
	GxSetBankForSubOBJ(sub_obj);
}
