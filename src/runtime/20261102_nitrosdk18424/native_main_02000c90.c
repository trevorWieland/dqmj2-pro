typedef signed long s32;
    typedef signed long long int s64;
typedef s32 fx32;
typedef s64 fx64;
    typedef union {
        struct {
            fx32 _00, _01;
            fx32 _10, _11;
        };
        fx32 m[2][2];
        fx32 a[4];
    } MtxFx22;
void native_main_02000c90(const MtxFx22 * pSrc, MtxFx22 * pDst, fx32 x, fx32 y);
inline fx32 mul64 (fx64 x, fx32 y)
{
	return (fx32)((x * y) >> 12 );
}
void native_main_02000c90 (const MtxFx22 *pSrc, MtxFx22 *pDst, fx32 x, fx32 y)
{
	fx64 v;
	((void) 0) ;
	((void) 0) ;
	v = (fx64)x;
	pDst->_00 = mul64(v, pSrc->_00);
	pDst->_01 = mul64(v, pSrc->_01);
	v = (fx64)y;
	pDst->_10 = mul64(v, pSrc->_10);
	pDst->_11 = mul64(v, pSrc->_11);
}
