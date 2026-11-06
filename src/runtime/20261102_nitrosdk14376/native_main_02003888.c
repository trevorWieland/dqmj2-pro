typedef unsigned short int u16;
    void native_main_02003888(int lcdc);
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
void native_data_main_02002da4 (int lcdc);
static inline void GxSetBankForLCDC (int lcdc)
{
	((void) 0) ;
	native_data_main_020e3304.vramCnt.lcdc |= lcdc;
	GX_StateCheck_VRAMCnt();
	native_data_main_02002da4(lcdc);
}
void native_main_02003888 (int lcdc)
{
	GxSetBankForLCDC(lcdc);
}
