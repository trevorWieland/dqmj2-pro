typedef unsigned long u32;
typedef signed long s32;
typedef volatile u32 vu32;
typedef vu32 REGType32v;
typedef s32 fx32;
    typedef union {
        struct {
            fx32 _00, _01, _02;
            fx32 _10, _11, _12;
            fx32 _20, _21, _22;
        };
        fx32 m[3][3];
        fx32 a[9];
    } MtxFx33;
int native_main_02004698(MtxFx33 * m);
static s32 G3X_IsGeometryBusy(void);
static inline s32 G3X_IsGeometryBusy (void)
{
	return (s32)((*( REGType32v *) (0x04000000 + 0x600)) & 0x08000000 );
}
void native_fn_02008d0c(register const void * pSrc, register void * pDest);
int native_main_02004698 (MtxFx33 *m)
{
	((void) 0) ;
	if (G3X_IsGeometryBusy()) {
		return -1;
	} else {
		native_fn_02008d0c((void *)((0x04000000 + 0x680) ), &m->_00);
		return 0;
	}
}
