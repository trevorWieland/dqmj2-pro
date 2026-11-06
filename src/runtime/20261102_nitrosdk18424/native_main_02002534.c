typedef signed long s32;
    typedef signed long long int s64;
typedef s32 fx32;
typedef s64 fx64;
typedef struct {
    fx32 x;
    fx32 y;
    fx32 z;
} VecFx32;
void native_main_02002534(const VecFx32 * a, const VecFx32 * b, VecFx32 * axb);
void native_main_02002534 (const VecFx32 *a, const VecFx32 *b, VecFx32 *axb)
{
	fx32 x, y, z;
	((void) 0) ;
	((void) 0) ;
	((void) 0) ;
	x = (fx32)(((fx64)a->y * b->z - (fx64)a->z * b->y + (1 << (12 - 1))) >> 12 );
	y = (fx32)(((fx64)a->z * b->x - (fx64)a->x * b->z + (1 << (12 - 1))) >> 12 );
	z = (fx32)(((fx64)a->x * b->y - (fx64)a->y * b->x + (1 << (12 - 1))) >> 12 );
	axb->x = x;
	axb->y = y;
	axb->z = z;
}
