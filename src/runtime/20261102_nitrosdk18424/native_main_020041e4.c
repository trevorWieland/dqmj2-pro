typedef unsigned short int u16;
typedef unsigned long u32;
typedef volatile u16 vu16;
typedef volatile u32 vu32;
typedef vu16 REGType16v;
typedef vu32 REGType32v;
void * native_main_020041e4(void);
typedef enum {
	GX_BGMODE_0 = 0,
	GX_BGMODE_1 = 1,
	GX_BGMODE_2 = 2,
	GX_BGMODE_3 = 3,
	GX_BGMODE_4 = 4,
	GX_BGMODE_5 = 5,
	GX_BGMODE_6 = 6
} GXBGMode;
void * native_main_020041e4 (void)
{
	GXBGMode bgMode = (GXBGMode)(((*( REGType32v *) (0x04000000 + 0x1000)) & 0x00000007 ) >> 0 );
	u32 bg = (*( REGType16v *) (0x04000000 + 0x100c)) ;
	if (bgMode < 5 || !(bg & 0x0080 )) {
		u32 blockID = (bg & 0x003c ) >> 2 ;
		return (void *)(0x06200000 + 0x4000 * blockID);
	} else {
		return ((void *)0) ;
	}
}
