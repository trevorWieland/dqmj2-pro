typedef unsigned long u32;
extern u32 native_data_main_020dcb44;
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
	GX_VRAM_TEX_NONE         = 0x0000,
	GX_VRAM_TEX_0_A          = GX_VRAM_A,
	GX_VRAM_TEX_0_B          = GX_VRAM_B,
	GX_VRAM_TEX_0_C          = GX_VRAM_C,
	GX_VRAM_TEX_0_D          = GX_VRAM_D,
	GX_VRAM_TEX_01_AB        = GX_VRAM_A | GX_VRAM_B,
	GX_VRAM_TEX_01_BC        = GX_VRAM_B | GX_VRAM_C,
	GX_VRAM_TEX_01_CD        = GX_VRAM_C | GX_VRAM_D,
	GX_VRAM_TEX_012_ABC      = GX_VRAM_A | GX_VRAM_B | GX_VRAM_C,
	GX_VRAM_TEX_012_BCD      = GX_VRAM_B | GX_VRAM_C | GX_VRAM_D,
	GX_VRAM_TEX_0123_ABCD    = GX_VRAM_A | GX_VRAM_B | GX_VRAM_C | GX_VRAM_D,
	GX_VRAM_TEX_01_AC        = GX_VRAM_A | GX_VRAM_C,
	GX_VRAM_TEX_01_AD        = GX_VRAM_A | GX_VRAM_D,
	GX_VRAM_TEX_01_BD        = GX_VRAM_B | GX_VRAM_D,
	GX_VRAM_TEX_012_ABD      = GX_VRAM_A | GX_VRAM_B | GX_VRAM_D,
	GX_VRAM_TEX_012_ACD      = GX_VRAM_A | GX_VRAM_C | GX_VRAM_D
} GXVRamTex;
typedef enum {
	GX_VRAM_CLEARIMAGE_NONE      = 0x0000,
	GX_VRAM_CLEARIMAGE_256_AB    = GX_VRAM_A | GX_VRAM_B,
	GX_VRAM_CLEARIMAGE_256_CD    = GX_VRAM_C | GX_VRAM_D,
	GX_VRAM_CLEARDEPTH_128_A     = GX_VRAM_A,
	GX_VRAM_CLEARDEPTH_128_B     = GX_VRAM_B,
	GX_VRAM_CLEARDEPTH_128_C     = GX_VRAM_C,
	GX_VRAM_CLEARDEPTH_128_D     = GX_VRAM_D
} GXVRamClearImage;
typedef enum {
	GX_VRAM_TEXPLTT_NONE          = 0x0000,
	GX_VRAM_TEXPLTT_0_F           = GX_VRAM_F,
	GX_VRAM_TEXPLTT_0_G           = GX_VRAM_G,
	GX_VRAM_TEXPLTT_01_FG         = GX_VRAM_F | GX_VRAM_G,
	GX_VRAM_TEXPLTT_0123_E        = GX_VRAM_E,
	GX_VRAM_TEXPLTT_01234_EF      = GX_VRAM_E | GX_VRAM_F,
	GX_VRAM_TEXPLTT_012345_EFG    = GX_VRAM_E | GX_VRAM_F | GX_VRAM_G
} GXVRamTexPltt;
void native_fn_020035c0(GXVRamTexPltt texPltt);
void native_main_020057a8(void);
void native_fn_02008714(u32 dmaNo);
static void GXi_WaitDma(u32 dmaNo);
typedef struct {
GXVRamClearImage field_0000;
u32 field_0004;
u32 field_0008;
GXVRamTexPltt field_000c;
u32 field_0010;
GXVRamTex field_0014;
u32 field_0018;
u32 field_001c;
} NativeStorage_020e333c;
extern NativeStorage_020e333c native_data_main_020e333c;
static inline void GXi_WaitDma (u32 dmaNo)
{
	if (dmaNo != ((u32) ~0) ) {
		native_fn_02008714(dmaNo);
	}
}
