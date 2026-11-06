typedef unsigned short int u16;
typedef unsigned long u32;
typedef signed long s32;
typedef volatile u16 vu16;
typedef volatile u32 vu32;
typedef vu16 REGType16v;
typedef vu32 REGType32v;
        typedef int BOOL;
typedef enum {
	GX_SHADING_TOON = 0,
	GX_SHADING_HIGHLIGHT = 1
} GXShading;
typedef enum {
	GX_FIFOINTR_COND_DISABLE      = 0,
	GX_FIFOINTR_COND_UNDERHALF    = 1,
	GX_FIFOINTR_COND_EMPTY        = 2
} GXFifoIntrCond;
void native_main_020043a0(void);
void native_fn_02004540(void);
void native_fn_0200470c(void);
static void G3X_SetShading(GXShading shading);
static void G3X_AlphaTest(BOOL enable, int ref);
static void G3X_AntiAlias(BOOL enable);
static void G3X_SetFifoIntrCond(GXFifoIntrCond cond);
static s32 G3X_IsGeometryBusy(void);
static void G3X_ResetMtxStackOverflow(void);
static void G3X_ResetLineBufferUnderflow(void);
static void G3X_ResetListRamOverflow(void);
void native_fn_02004518(void);
static inline void G3X_SetShading (GXShading shading)
{
	(*( REGType16v *) (0x04000000 + 0x060)) = (u16)(((*( REGType16v *) (0x04000000 + 0x060)) & ~(0x0002 |
	                                                 0x1000 |
	                                                 0x2000 )) |
	                          (shading << 1 ));
}
static inline void G3X_AlphaTest (BOOL enable, int ref)
{
	if (enable) {
		((void) 0) ;
		(*( REGType16v *) (0x04000000 + 0x060)) = (u16)((*( REGType16v *) (0x04000000 + 0x060)) &
		                          ~(0x1000 | 0x2000 ) |
		                          0x0004 );
		(*( REGType16v *) (0x04000000 + 0x340)) = (u16)ref;
	} else {
		(*( REGType16v *) (0x04000000 + 0x060)) &= (u16) ~(0x0004 |
		                             0x1000 | 0x2000 );
	}
}
static inline void G3X_AntiAlias (BOOL enable)
{
	if (enable) {
		(*( REGType16v *) (0x04000000 + 0x060)) = (u16)((*( REGType16v *) (0x04000000 + 0x060)) &
		                          ~(0x1000 | 0x2000 ) |
		                          0x0010 );
	} else {
		(*( REGType16v *) (0x04000000 + 0x060)) &= (u16) ~(0x0010 |
		                             0x1000 | 0x2000 );
	}
}
static inline void G3X_SetFifoIntrCond (GXFifoIntrCond cond)
{
	((void) 0) ;
	(*( REGType32v *) (0x04000000 + 0x600)) = (((*( REGType32v *) (0x04000000 + 0x600)) & ~0xc0000000 ) |
	                  (cond << 30 ));
}
static inline s32 G3X_IsGeometryBusy (void)
{
	return (s32)((*( REGType32v *) (0x04000000 + 0x600)) & 0x08000000 );
}
static inline void G3X_ResetMtxStackOverflow (void)
{
	(*( REGType32v *) (0x04000000 + 0x600)) |= 0x00008000 ;
}
static inline void G3X_ResetLineBufferUnderflow (void)
{
	(*( REGType16v *) (0x04000000 + 0x060)) |= 0x1000 ;
}
static inline void G3X_ResetListRamOverflow (void)
{
	(*( REGType16v *) (0x04000000 + 0x060)) |= 0x2000 ;
}
typedef enum {
	GX_LIGHTMASK_NONE    = 0,
	GX_LIGHTMASK_0       = 1,
	GX_LIGHTMASK_1       = 2,
	GX_LIGHTMASK_01      = 3,
	GX_LIGHTMASK_2       = 4,
	GX_LIGHTMASK_02      = 5,
	GX_LIGHTMASK_12      = 6,
	GX_LIGHTMASK_012     = 7,
	GX_LIGHTMASK_3       = 8,
	GX_LIGHTMASK_03      = 9,
	GX_LIGHTMASK_13      = 10,
	GX_LIGHTMASK_013     = 11,
	GX_LIGHTMASK_23      = 12,
	GX_LIGHTMASK_023     = 13,
	GX_LIGHTMASK_123     = 14,
	GX_LIGHTMASK_0123    = 15
} GXLightMask;
typedef enum {
	GX_POLYGONMODE_MODULATE    = 0,
	GX_POLYGONMODE_DECAL       = 1,
	GX_POLYGONMODE_TOON        = 2,
	GX_POLYGONMODE_SHADOW      = 3
} GXPolygonMode;
typedef enum {
	GX_CULL_ALL      = 0,
	GX_CULL_FRONT    = 1,
	GX_CULL_BACK     = 2,
	GX_CULL_NONE     = 3
} GXCull;
typedef enum {
	GX_POLYGON_ATTR_MISC_NONE                = 0,
	GX_POLYGON_ATTR_MISC_XLU_DEPTH_UPDATE    = 1 << 11 ,
	GX_POLYGON_ATTR_MISC_FAR_CLIPPING        = 1 << 12 ,
	GX_POLYGON_ATTR_MISC_DISP_1DOT           = 1 << 13 ,
	GX_POLYGON_ATTR_MISC_DEPTHTEST_DECAL     = 1 << 14 ,
	GX_POLYGON_ATTR_MISC_FOG                 = 1 << 15
} GXPolygonAttrMisc;
typedef enum {
	GX_TEXREPEAT_NONE    = 0,
	GX_TEXREPEAT_S       = 1,
	GX_TEXREPEAT_T       = 2,
	GX_TEXREPEAT_ST      = 3
} GXTexRepeat;
typedef enum {
	GX_TEXFLIP_NONE    = 0,
	GX_TEXFLIP_S       = 1,
	GX_TEXFLIP_T       = 2,
	GX_TEXFLIP_ST      = 3
} GXTexFlip;
typedef enum {
	GX_TEXSIZE_S8       = 0,
	GX_TEXSIZE_S16      = 1,
	GX_TEXSIZE_S32      = 2,
	GX_TEXSIZE_S64      = 3,
	GX_TEXSIZE_S128     = 4,
	GX_TEXSIZE_S256     = 5,
	GX_TEXSIZE_S512     = 6,
	GX_TEXSIZE_S1024    = 7
} GXTexSizeS;
typedef enum {
	GX_TEXSIZE_T8       = 0,
	GX_TEXSIZE_T16      = 1,
	GX_TEXSIZE_T32      = 2,
	GX_TEXSIZE_T64      = 3,
	GX_TEXSIZE_T128     = 4,
	GX_TEXSIZE_T256     = 5,
	GX_TEXSIZE_T512     = 6,
	GX_TEXSIZE_T1024    = 7
} GXTexSizeT;
typedef enum {
	GX_TEXFMT_NONE       = 0,
	GX_TEXFMT_A3I5       = 1,
	GX_TEXFMT_PLTT4      = 2,
	GX_TEXFMT_PLTT16     = 3,
	GX_TEXFMT_PLTT256    = 4,
	GX_TEXFMT_COMP4x4    = 5,
	GX_TEXFMT_A5I3       = 6,
	GX_TEXFMT_DIRECT     = 7
} GXTexFmt;
typedef enum {
	GX_TEXPLTTCOLOR0_USE  = 0,
	GX_TEXPLTTCOLOR0_TRNS = 1
} GXTexPlttColor0;
typedef enum {
	GX_TEXGEN_NONE        = 0,
	GX_TEXGEN_TEXCOORD    = 1,
	GX_TEXGEN_NORMAL      = 2,
	GX_TEXGEN_VERTEX      = 3
} GXTexGen;
static void G3_Direct1(int op, u32 param0);
static void G3_PolygonAttr(int light, GXPolygonMode polyMode, GXCull cullMode, int polygonID, int alpha, int misc);
static void G3_TexImageParam(GXTexFmt texFmt,
                             GXTexGen texGen,
                             GXTexSizeS s,
                             GXTexSizeT t,
                             GXTexRepeat repeat, GXTexFlip flip, GXTexPlttColor0 pltt0, u32 addr);
static void G3_End(void);
static inline void G3_Direct1 (int op, u32 param0)
{
	*(REGType32v *)((0x04000000 + 0x440) + ((op - 0x10 ) * 4)) = param0;
}
static inline void G3_PolygonAttr (int light, GXPolygonMode polyMode, GXCull cullMode, int polygonID, int alpha, int misc
                                   )
{
	((void) 0) ;
	((void) 0) ;
	((void) 0) ;
	((void) 0) ;
	((void) 0) ;
	(*( REGType32v *) (0x04000000 + 0x4a4)) = ((u32)(((light) << 0) | (( polyMode) << 4) | (( cullMode) << 6) | ( misc) | (( polygonID) << 24) | (( alpha) << 16)))
	                                                ;
}
static inline void G3_TexImageParam (GXTexFmt texFmt,
                                     GXTexGen texGen,
                                     GXTexSizeS s,
                                     GXTexSizeT t,
                                     GXTexRepeat repeat,
                                     GXTexFlip flip, GXTexPlttColor0 pltt0, u32 addr)
{
	((void) 0) ;
	((void) 0) ;
	((void) 0) ;
	((void) 0) ;
	((void) 0) ;
	((void) 0) ;
	((void) 0) ;
	((void) 0) ;
	(*( REGType32v *) (0x04000000 + 0x4a8)) = ((u32)((( addr) >> 3) | ((texFmt) << 26) | (( texGen) << 30) | (( s) << 20) | (( t) << 23) | (( repeat) << 16) | (( flip) << 18) | (( pltt0) << 29))) ;
}
static inline void G3_End (void)
{
	(*( REGType32v *) (0x04000000 + 0x504)) = 0;
}
static void G2_SetBG0Priority(int priority);
static inline void G2_SetBG0Priority (int priority)
{
	((void) 0) ;
	(*( REGType16v *) (0x04000000 + 0x008)) = (u16)(((*( REGType16v *) (0x04000000 + 0x008)) & ~0x0003 ) |
	                      (priority << 0 ));
}
void native_main_020043a0 (void)
{
	native_fn_02004518();
	G3_End();
	while ( G3X_IsGeometryBusy()) {
	}
	(*( REGType16v *) (0x04000000 + 0x060)) = 0;
	(*( REGType32v *) (0x04000000 + 0x600)) = 0;
	(*( REGType32v *) (0x04000000 + 0x010)) = 0;
	G3X_ResetListRamOverflow();
	G3X_ResetLineBufferUnderflow();
	G3X_SetShading(GX_SHADING_TOON);
	G3X_AntiAlias(1 );
	G3X_AlphaTest(0 , 0);
	G3X_ResetMtxStackOverflow();
	G3X_SetFifoIntrCond(GX_FIFOINTR_COND_EMPTY);
	native_fn_02004540();
	(*( REGType32v *) (0x04000000 + 0x350)) = 0;
	(*( REGType16v *) (0x04000000 + 0x354)) = 0x7fff;
	(*( REGType16v *) (0x04000000 + 0x356)) = 0;
	(*( REGType32v *) (0x04000000 + 0x358)) = 0;
	(*( REGType16v *) (0x04000000 + 0x35c)) = 0;
	G2_SetBG0Priority(0);
	native_fn_0200470c();
	G3_PolygonAttr(GX_LIGHTMASK_NONE, GX_POLYGONMODE_MODULATE, GX_CULL_BACK, 0, 31, GX_POLYGON_ATTR_MISC_NONE);
	G3_TexImageParam(GX_TEXFMT_NONE,
	                 GX_TEXGEN_NONE,
	                 GX_TEXSIZE_S8, GX_TEXSIZE_T8, GX_TEXREPEAT_NONE, GX_TEXFLIP_NONE, GX_TEXPLTTCOLOR0_USE, 0);
	G3_Direct1(0x2b , 0);
}
void native_fn_02004518 (void);
void native_fn_02004540 (void);
void native_fn_0200470c (void);
