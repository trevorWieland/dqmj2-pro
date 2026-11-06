typedef unsigned char u8;
typedef unsigned short int u16;
typedef volatile u8 vu8;
typedef volatile u16 vu16;
typedef vu8 REGType8v;
typedef vu16 REGType16v;
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
	GX_VRAM_CLEARIMAGE_NONE      = 0x0000,
	GX_VRAM_CLEARIMAGE_256_AB    = GX_VRAM_A | GX_VRAM_B,
	GX_VRAM_CLEARIMAGE_256_CD    = GX_VRAM_C | GX_VRAM_D,
	GX_VRAM_CLEARDEPTH_128_A     = GX_VRAM_A,
	GX_VRAM_CLEARDEPTH_128_B     = GX_VRAM_B,
	GX_VRAM_CLEARDEPTH_128_C     = GX_VRAM_C,
	GX_VRAM_CLEARDEPTH_128_D     = GX_VRAM_D
} GXVRamClearImage;
    void native_main_020036a8(GXVRamClearImage clrImg);
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
void native_fn_02002da4 (int lcdc);
static inline void clearImageOn_ (void)
{
	(*( REGType16v *) (0x04000000 + 0x060)) |= 0x4000 ;
}
static inline void clearImageOff_ (void)
{
	(*( REGType16v *) (0x04000000 + 0x060)) &= ~0x4000 ;
}
static inline void GX_VRAMCNT_SetCLRIMG_ (GXVRamClearImage clrImg)
{
	switch (clrImg) {
	case GX_VRAM_CLEARIMAGE_256_AB:
		(*( REGType8v *) (0x04000000 + 0x240)) = (u8)GX_VRAMCNT_A_TEX_2;
	case GX_VRAM_CLEARDEPTH_128_B:
		(*( REGType8v *) (0x04000000 + 0x241)) = (u8)GX_VRAMCNT_B_TEX_3;
		clearImageOn_();
		break;
	case GX_VRAM_CLEARIMAGE_256_CD:
		(*( REGType8v *) (0x04000000 + 0x242)) = (u8)GX_VRAMCNT_C_TEX_2;
	case GX_VRAM_CLEARDEPTH_128_D:
		(*( REGType8v *) (0x04000000 + 0x243)) = (u8)GX_VRAMCNT_D_TEX_3;
		clearImageOn_();
		break;
	case GX_VRAM_CLEARIMAGE_NONE:
		clearImageOff_();
		break;
	case GX_VRAM_CLEARDEPTH_128_A:
		(*( REGType8v *) (0x04000000 + 0x240)) = (u8)GX_VRAMCNT_A_TEX_3;
		clearImageOn_();
		break;
	case GX_VRAM_CLEARDEPTH_128_C:
		(*( REGType8v *) (0x04000000 + 0x242)) = (u8)GX_VRAMCNT_C_TEX_3;
		clearImageOn_();
		break;
	default:
		((void) 0) ;
		break;
	}
}
static inline void GxSetBankForClearImage (GXVRamClearImage clrImg)
{
	((void) 0) ;
	native_data_main_020e3304.vramCnt.lcdc = (u16)(~clrImg & (native_data_main_020e3304.vramCnt.lcdc | native_data_main_020e3304.vramCnt.clrImg));
	native_data_main_020e3304.vramCnt.clrImg = clrImg;
	GX_StateCheck_VRAMCnt();
	GX_VRAMCNT_SetCLRIMG_(clrImg);
	native_fn_02002da4(native_data_main_020e3304.vramCnt.lcdc);
}
void native_main_020036a8 (GXVRamClearImage clrImg)
{
	GxSetBankForClearImage(clrImg);
}
