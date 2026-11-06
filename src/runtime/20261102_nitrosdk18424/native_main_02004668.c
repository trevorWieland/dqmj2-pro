typedef unsigned long u32;
typedef signed long s32;
typedef volatile u32 vu32;
typedef vu32 REGType32v;
typedef s32 fx32;
    typedef union {
        struct {
            fx32 _00, _01, _02, _03;
            fx32 _10, _11, _12, _13;
            fx32 _20, _21, _22, _23;
            fx32 _30, _31, _32, _33;
        };
        fx32 m[4][4];
        fx32 a[16];
    } MtxFx44;
int native_main_02004668(MtxFx44 * m);
static s32 G3X_IsGeometryBusy(void);
static inline s32 G3X_IsGeometryBusy (void)
{
	return (s32)((*( REGType32v *) (0x04000000 + 0x600)) & 0x08000000 );
}
void native_fn_02008d4c(register const void * pSrc, register void * pDest);
int native_main_02004668 (MtxFx44 *m)
{
	((void) 0) ;
	if (G3X_IsGeometryBusy()) {
		return -1;
	} else {
		native_fn_02008d4c((void *)(0x04000000 + 0x640) , &m->_00);
		return 0;
	}
}
