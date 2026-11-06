typedef unsigned long u32;
typedef signed long s32;
typedef volatile u32 vu32;
typedef vu32 REGType32v;
void native_main_020045d8(void);
int native_fn_020047ac(s32 * level);
int native_fn_020047dc(s32 * level);
static void G3X_ResetMtxStackOverflow(void);
static inline void G3X_ResetMtxStackOverflow (void)
{
	(*( REGType32v *) (0x04000000 + 0x600)) |= 0x00008000 ;
}
typedef enum {
	GX_MTXMODE_PROJECTION      = 0,
	GX_MTXMODE_POSITION        = 1,
	GX_MTXMODE_POSITION_VECTOR = 2,
	GX_MTXMODE_TEXTURE         = 3
} GXMtxMode;
static void G3_MtxMode(GXMtxMode mode);
static void G3_PopMtx(int num);
static void G3_Identity(void);
static inline void G3_MtxMode (GXMtxMode mode)
{
	((void) 0) ;
	(*( REGType32v *) (0x04000000 + 0x440)) = ((u32) ((mode) << 0)) ;
}
static inline void G3_PopMtx (int num)
{
	((void) 0) ;
	(*( REGType32v *) (0x04000000 + 0x448)) = ((u32) (num)) ;
}
static inline void G3_Identity ()
{
	(*( REGType32v *) (0x04000000 + 0x454)) = 0;
}
void native_main_020045d8 (void)
{
	s32 levelPV;
	s32 levelPJ;
	G3X_ResetMtxStackOverflow();
	while (native_fn_020047ac(&levelPV))
		;
	while (native_fn_020047dc(&levelPJ))
		;
	G3_MtxMode(GX_MTXMODE_TEXTURE);
	G3_Identity();
	G3_MtxMode(GX_MTXMODE_PROJECTION);
	if (levelPJ != 0) {
		G3_PopMtx(levelPJ);
	}
	G3_MtxMode(GX_MTXMODE_POSITION_VECTOR);
	G3_PopMtx(levelPV);
	G3_Identity();
}
int native_fn_020047ac (s32 *level);
int native_fn_020047dc (s32 *level);
