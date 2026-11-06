typedef signed long s32;
    typedef signed long long int s64;
typedef s32 fx32;
typedef s64 fx64;
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
void native_main_02001bac(const MtxFx44 * a, const MtxFx44 * b, MtxFx44 * ab);
void native_main_02001bac (const MtxFx44 *a, const MtxFx44 *b, MtxFx44 *ab)
{
	MtxFx44 tmp;
	MtxFx44 *p;
	register fx32 x, y, z, w;
	register fx32 xx, yy, zz, ww;
	((void) 0) ;
	((void) 0) ;
	((void) 0) ;
	if (ab == b) {
		p = &tmp;
	} else {
		p = ab;
	}
	x = a->_00;
	y = a->_01;
	z = a->_02;
	w = a->_03;
	p->_00 = (fx32)(((fx64)x * b->_00 + (fx64)y * b->_10 + (fx64)z * b->_20 + (fx64)w * b->_30) >> 12 );
	p->_01 = (fx32)(((fx64)x * b->_01 + (fx64)y * b->_11 + (fx64)z * b->_21 + (fx64)w * b->_31) >> 12 );
	p->_03 = (fx32)(((fx64)x * b->_03 + (fx64)y * b->_13 + (fx64)z * b->_23 + (fx64)w * b->_33) >> 12 );
	xx = b->_02;
	yy = b->_12;
	zz = b->_22;
	ww = b->_32;
	p->_02 = (fx32)(((fx64)x * xx + (fx64)y * yy + (fx64)z * zz + (fx64)w * ww) >> 12 );
	x = a->_10;
	y = a->_11;
	z = a->_12;
	w = a->_13;
	p->_12 = (fx32)(((fx64)x * xx + (fx64)y * yy + (fx64)z * zz + (fx64)w * ww) >> 12 );
	p->_11 = (fx32)(((fx64)x * b->_01 + (fx64)y * b->_11 + (fx64)z * b->_21 + (fx64)w * b->_31) >> 12 );
	p->_13 = (fx32)(((fx64)x * b->_03 + (fx64)y * b->_13 + (fx64)z * b->_23 + (fx64)w * b->_33) >> 12 );
	xx = b->_00;
	yy = b->_10;
	zz = b->_20;
	ww = b->_30;
	p->_10 = (fx32)(((fx64)x * xx + (fx64)y * yy + (fx64)z * zz + (fx64)w * ww) >> 12 );
	x = a->_20;
	y = a->_21;
	z = a->_22;
	w = a->_23;
	p->_20 = (fx32)(((fx64)x * xx + (fx64)y * yy + (fx64)z * zz + (fx64)w * ww) >> 12 );
	p->_21 = (fx32)(((fx64)x * b->_01 + (fx64)y * b->_11 + (fx64)z * b->_21 + (fx64)w * b->_31) >> 12 );
	p->_23 = (fx32)(((fx64)x * b->_03 + (fx64)y * b->_13 + (fx64)z * b->_23 + (fx64)w * b->_33) >> 12 );
	xx = b->_02;
	yy = b->_12;
	zz = b->_22;
	ww = b->_32;
	p->_22 = (fx32)(((fx64)x * xx + (fx64)y * yy + (fx64)z * zz + (fx64)w * ww) >> 12 );
	x = a->_30;
	y = a->_31;
	z = a->_32;
	w = a->_33;
	p->_32 = (fx32)(((fx64)x * xx + (fx64)y * yy + (fx64)z * zz + (fx64)w * ww) >> 12 );
	p->_31 = (fx32)(((fx64)x * b->_01 + (fx64)y * b->_11 + (fx64)z * b->_21 + (fx64)w * b->_31) >> 12 );
	p->_30 = (fx32)(((fx64)x * b->_00 + (fx64)y * b->_10 + (fx64)z * b->_20 + (fx64)w * b->_30) >> 12 );
	p->_33 = (fx32)(((fx64)x * b->_03 + (fx64)y * b->_13 + (fx64)z * b->_23 + (fx64)w * b->_33) >> 12 );
	if (p == &tmp) {
		*ab = tmp;
	}
}
