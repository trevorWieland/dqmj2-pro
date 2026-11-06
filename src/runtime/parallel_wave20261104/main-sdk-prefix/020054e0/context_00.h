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
	GX_VRAM_BGEXTPLTT_NONE       = 0x0000,
	GX_VRAM_BGEXTPLTT_01_F       = GX_VRAM_F,
	GX_VRAM_BGEXTPLTT_23_G       = GX_VRAM_G,
	GX_VRAM_BGEXTPLTT_0123_E     = GX_VRAM_E,
	GX_VRAM_BGEXTPLTT_0123_FG    = GX_VRAM_F | GX_VRAM_G
} GXVRamBGExtPltt;
typedef enum {
	GX_VRAM_OBJEXTPLTT_NONE    = 0,
	GX_VRAM_OBJEXTPLTT_0_F     = GX_VRAM_F,
	GX_VRAM_OBJEXTPLTT_0_G     = GX_VRAM_G
} GXVRamOBJExtPltt;
typedef enum {
	GX_VRAM_SUB_BGEXTPLTT_NONE = 0x0000,
	GX_VRAM_SUB_BGEXTPLTT_0123_H = GX_VRAM_H
} GXVRamSubBGExtPltt;
typedef enum {
	GX_VRAM_SUB_OBJEXTPLTT_NONE = 0x0000,
	GX_VRAM_SUB_OBJEXTPLTT_0_I = GX_VRAM_I
} GXVRamSubOBJExtPltt;
void native_fn_02003a40(GXVRamSubOBJExtPltt sub_objExtPltt);
void native_main_020054e0(void);
void native_fn_02008714(u32 dmaNo);
static void GXi_WaitDma(u32 dmaNo);
typedef struct {
GXVRamSubBGExtPltt field_0000;
u32 field_0004;
GXVRamOBJExtPltt field_0008;
u32 field_000c;
u32 field_0010;
GXVRamBGExtPltt field_0014;
GXVRamSubOBJExtPltt field_0018;
} NativeStorage_020e3320;
extern NativeStorage_020e3320 native_data_main_020e3320;
static inline void GXi_WaitDma (u32 dmaNo)
{
	if (dmaNo != ((u32) ~0) ) {
		native_fn_02008714(dmaNo);
	}
}
