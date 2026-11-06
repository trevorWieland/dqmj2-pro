typedef unsigned short int u16;
typedef unsigned long u32;
typedef volatile u16 vu16;
typedef volatile u32 vu32;
typedef vu16 REGType16v;
typedef vu32 REGType32v;
void * native_main_02003ff4(void);
typedef enum {
	GX_BGMODE_0 = 0,
	GX_BGMODE_1 = 1,
	GX_BGMODE_2 = 2,
	GX_BGMODE_3 = 3,
	GX_BGMODE_4 = 4,
	GX_BGMODE_5 = 5,
	GX_BGMODE_6 = 6
} GXBGMode;
static inline int getBGScreenOffset_ (void)
{
	return (int)(0x10000 * (((*( REGType32v *) (0x04000000 + 0x000)) & 0x38000000 ) >>
	                        27 ));
}
void *native_main_02003ff4 (void)
{
	GXBGMode bgMode = (GXBGMode)(((*( REGType32v *) (0x04000000 + 0x000)) & 0x00000007 ) >> 0 );
	u32 bg = (*( REGType16v *) (0x04000000 + 0x00e)) ;
	int offset = getBGScreenOffset_();
	u32 blockID = (bg & 0x1f00 ) >> 8 ;
	switch (bgMode) {
	case GX_BGMODE_0:
	case GX_BGMODE_1:
	case GX_BGMODE_2:
		return (void *)(0x06000000 + offset + 0x800 * blockID);
		break;
	case GX_BGMODE_3:
	case GX_BGMODE_4:
	case GX_BGMODE_5:
		if (bg & 0x0080 ) {
			return (void *)(0x06000000 + 0x4000 * blockID);
		} else {
			return (void *)(0x06000000 + offset + 0x800 * blockID);
		}
		break;
	case GX_BGMODE_6:
		return ((void *)0) ;
		break;
	default:
		((void) 0) ;
		return ((void *)0) ;
		break;
	}
}
