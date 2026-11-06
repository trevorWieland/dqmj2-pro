#include "context_00.h"
void native_main_02002210 (fx32 fovySin, fx32 fovyCos, fx32 aspect, fx32 n, fx32 f, fx32 scaleW, MtxFx44 *mtx)
{
	fx32 one_tan;
	fx64 t;
	((void) 0) ;
	((void) 0) ;
	((void) 0) ;
	((void) 0) ;
	((void) 0) ;
	((void) 0) ;
	one_tan = native_fn_0200235c((fx32)fovyCos, (fx32)fovySin);
	FX_InvAsyncImm(n - f);
	if (scaleW != ((fx32) 0x0000000000001000L) ) {
		one_tan = (one_tan * scaleW) / ((fx32) 0x0000000000001000L) ;
	}
	mtx->_01 = 0;
	mtx->_02 = 0;
	mtx->_03 = 0;
	mtx->_10 = 0;
	mtx->_11 = one_tan;
	mtx->_12 = 0;
	mtx->_13 = 0;
	mtx->_20 = 0;
	mtx->_21 = 0;
	mtx->_23 = -scaleW;
	mtx->_30 = 0;
	mtx->_31 = 0;
	mtx->_33 = 0;
	t = FX_GetInvResultFx64c();
	FX_DivAsyncImm(one_tan, aspect);
	if (scaleW != ((fx32) 0x0000000000001000L) ) {
		t = (t * scaleW) / ((fx32) 0x0000000000001000L) ;
	}
	mtx->_22 = FX_Mul32x64cInline (f + n, t) ;
	mtx->_32 = FX_Mul32x64cInline (FX_MulInline (n << 1, f), t) ;
	mtx->_00 = native_fn_020023c4();
}
