typedef unsigned char u8;
typedef unsigned short int u16;
typedef unsigned long u32;
typedef volatile u8 vu8;
typedef volatile u32 vu32;
typedef vu8 REGType8v;
typedef vu32 REGType32v;
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
	GX_VRAM_SUB_BGEXTPLTT_NONE = 0x0000,
	GX_VRAM_SUB_BGEXTPLTT_0123_H = GX_VRAM_H
} GXVRamSubBGExtPltt;
    void native_main_020039c0(GXVRamSubBGExtPltt sub_bgExtPltt);
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
	GX_VRAMCNT_H_DISABLE           = 0,
	GX_VRAMCNT_H_LCDC_0x06898000   = (0 << 0 ) | (1 << 7 ),
	GX_VRAMCNT_H_SUBBG_0x06200000  = (1 << 0 ) | (1 << 7 ),
	GX_VRAMCNT_H_SUBBGEXTPLTT_0123 = (2 << 0 ) | (1 << 7 )
} GX_VRAMCNT_H;
void native_fn_02002da4 (int lcdc);
static inline void subBGExtPlttOn_ (void)
{
	(*( REGType32v *) (0x04000000 + 0x1000)) |= 0x40000000 ;
}
static inline void subBGExtPlttOff_ (void)
{
	(*( REGType32v *) (0x04000000 + 0x1000)) &= ~0x40000000 ;
}
static inline void GX_VRAMCNT_SetSubBGExtPltt_ (GXVRamSubBGExtPltt bgExtPltt)
{
	switch (bgExtPltt) {
	case GX_VRAM_SUB_BGEXTPLTT_0123_H:
		subBGExtPlttOn_();
		(*( REGType8v *) (0x04000000 + 0x248)) = GX_VRAMCNT_H_SUBBGEXTPLTT_0123;
		break;
	case GX_VRAM_SUB_BGEXTPLTT_NONE:
		subBGExtPlttOff_();
		break;
	default:
		((void) 0) ;
		break;
	}
}
static inline void GxSetBankForSubBGExtPltt (GXVRamSubBGExtPltt sub_bgExtPltt)
{
	((void) 0) ;
	native_data_main_020e3304.vramCnt.lcdc = (u16)(~sub_bgExtPltt & (native_data_main_020e3304.vramCnt.lcdc | native_data_main_020e3304.vramCnt.sub_bgExtPltt));
	native_data_main_020e3304.vramCnt.sub_bgExtPltt = sub_bgExtPltt;
	GX_StateCheck_VRAMCnt();
	GX_VRAMCNT_SetSubBGExtPltt_(sub_bgExtPltt);
	native_fn_02002da4(native_data_main_020e3304.vramCnt.lcdc);
}
void native_main_020039c0 (GXVRamSubBGExtPltt sub_bgExtPltt)
{
	GxSetBankForSubBGExtPltt(sub_bgExtPltt);
}
