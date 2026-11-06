typedef signed long s32;
typedef s32 fx32;
typedef struct {
    fx32 x;
    fx32 y;
    fx32 z;
} VecFx32;
    typedef union {
        struct {
            fx32 _00, _01, _02;
            fx32 _10, _11, _12;
            fx32 _20, _21, _22;
            fx32 _30, _31, _32;
        };
        fx32 m[4][3];
        fx32 a[12];
    } MtxFx43;
void native_main_02001848(const VecFx32 * camPos, const VecFx32 * camUp, const VecFx32 * target, MtxFx43 * mtx);
fx32 native_fn_020024f8(const VecFx32 * a, const VecFx32 * b);
void native_fn_02002534(const VecFx32 * a, const VecFx32 * b, VecFx32 * axb);
void native_fn_02002618(const VecFx32 * pSrc, VecFx32 * pDst);
void native_main_02001848 (const VecFx32 *camPos, const VecFx32 *camUp, const VecFx32 *target, MtxFx43 *mtx)
{
	VecFx32 vLook, vRight, vUp;
	((void) 0) ;
	((void) 0) ;
	((void) 0) ;
	((void) 0) ;
	vLook.x = camPos->x - target->x;
	vLook.y = camPos->y - target->y;
	vLook.z = camPos->z - target->z;
	native_fn_02002618(&vLook, &vLook);
	native_fn_02002534(camUp, &vLook, &vRight);
	native_fn_02002618(&vRight, &vRight);
	native_fn_02002534(&vLook, &vRight, &vUp);
	mtx->_00 = vRight.x;
	mtx->_01 = vUp.x;
	mtx->_02 = vLook.x;
	mtx->_10 = vRight.y;
	mtx->_11 = vUp.y;
	mtx->_12 = vLook.y;
	mtx->_20 = vRight.z;
	mtx->_21 = vUp.z;
	mtx->_22 = vLook.z;
	mtx->_30 = -native_fn_020024f8(camPos, &vRight);
	mtx->_31 = -native_fn_020024f8(camPos, &vUp);
	mtx->_32 = -native_fn_020024f8(camPos, &vLook);
}
