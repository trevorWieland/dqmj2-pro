typedef signed long s32;
    typedef signed long long int s64;
typedef s32 fx32;
typedef s64 fx64;
typedef struct {
    fx32 x;
    fx32 y;
    fx32 z;
} VecFx32;
fx32 native_main_020024f8(const VecFx32 * a, const VecFx32 * b);
fx32 native_main_020024f8 (const VecFx32 *a, const VecFx32 *b)
{
	((void) 0) ;
	((void) 0) ;
	return (fx32)(((fx64)a->x * b->x +
	               (fx64)a->y * b->y + (fx64)a->z * b->z + (1 << (12 - 1))) >> 12 );
}
