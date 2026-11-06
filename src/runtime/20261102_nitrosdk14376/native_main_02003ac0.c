typedef unsigned short int u16;
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
void native_fn_02002da4 (int lcdc);
int native_main_02003ac0 (u16 *g3bit)
{
	int rval = *g3bit;
	*g3bit = 0;
	native_data_main_020e3304.vramCnt.lcdc |= rval;
	native_fn_02002da4(rval);
	return rval;
}
