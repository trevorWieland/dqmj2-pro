typedef unsigned short int u16;
typedef unsigned long u32;
typedef volatile u32 vu32;
typedef vu32 REGType32v;
typedef enum {
	GX_BGMODE_0 = 0,
	GX_BGMODE_1 = 1,
	GX_BGMODE_2 = 2,
	GX_BGMODE_3 = 3,
	GX_BGMODE_4 = 4,
	GX_BGMODE_5 = 5,
	GX_BGMODE_6 = 6
} GXBGMode;
typedef enum {
	GX_BG0_AS_2D = 0,
	GX_BG0_AS_3D = 1
} GXBG0As;
typedef enum {
	GX_DISPMODE_GRAPHICS = 0x01,
	GX_DISPMODE_VRAM_A = 0x02,
	GX_DISPMODE_VRAM_B = 0x06,
	GX_DISPMODE_VRAM_C = 0x0a,
	GX_DISPMODE_VRAM_D = 0x0e,
	GX_DISPMODE_MMEM = 0x03
} GXDispMode;
void native_main_02002c98(GXDispMode dispMode, GXBGMode bgMode, GXBG0As bg0_2d3d);
extern u16 native_data_main_020e3300;
extern u16 native_data_main_020dcb40;
void native_main_02002c98 (GXDispMode dispMode, GXBGMode bgMode, GXBG0As bg0_2d3d)
{
	u32 cnt = (*( REGType32v *) (0x04000000 + 0x000)) ;
	((void) 0) ;
	((void) 0)
	            ;
	native_data_main_020e3300 = (u16)dispMode;
	if (!native_data_main_020dcb40) {
		dispMode = ((GXDispMode)0x00) ;
	}
	((void) 0) ;
	((void) 0) ;
	cnt &= ~(0x00000007 |
	         0x00000008 | 0x00030000 | 0x000c0000 );
	(*( REGType32v *) (0x04000000 + 0x000)) = (u32)(cnt |
	                       (dispMode << 16 ) |
	                       (bgMode << 0 ) | (bg0_2d3d <<
	                                                                  3 ));
	if (native_data_main_020e3300 == ((GXDispMode)0x00) ) {
		native_data_main_020dcb40 = 0 ;
	}
}
