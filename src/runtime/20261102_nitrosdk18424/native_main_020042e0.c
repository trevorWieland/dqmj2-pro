typedef unsigned short int u16;
typedef unsigned long u32;
typedef volatile u16 vu16;
void native_main_020042e0(u32 addr, int plane, int brightness);
typedef enum {
	G2_BLENDTYPE_NONE    = 0x0000,
	G2_BLENDTYPE_ALPHA   = 0x0040,
	G2_BLENDTYPE_FADEIN  = 0x0080,
	G2_BLENDTYPE_FADEOUT = 0x00c0
} G2_BLENDTYPE;
void native_main_020042e0 (u32 addr, int plane, int brightness)
{
	((void) 0) ;
	((void) 0) ;
	if (brightness < 0) {
		*((vu16 *)addr + 0) = (u16)(G2_BLENDTYPE_FADEOUT | plane);
		*((vu16 *)addr + 2) = (u16) - brightness;
	} else {
		*((vu16 *)addr + 0) = (u16)(G2_BLENDTYPE_FADEIN | plane);
		*((vu16 *)addr + 2) = (u16)brightness;
	}
}
