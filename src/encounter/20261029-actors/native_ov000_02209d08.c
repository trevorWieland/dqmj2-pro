#include "actor_context.h"
extern ActorGlobal native_ov000_data_022385b8;
extern void native_fn_02000ce8(Matrix33 *matrix);
extern void native_fn_02027fe8(Matrix33 *matrix, s32 value);
extern void native_fn_02028044(Matrix33 *matrix, s32 value);
extern void native_fn_02000e1c(const Matrix33 *left, const Matrix33 *right, Matrix33 *result);
extern void native_fn_0200103c(const Vector3 *vector, const Matrix33 *matrix, Vector3 *result);
void native_ov000_02209d08(Actor *actor)
{
    Matrix33 first;
    Matrix33 second;
    Matrix33 third;
    native_fn_02000ce8(&first);
    native_fn_02000ce8(&second);
    native_fn_02000ce8(&third);
    native_fn_02027fe8(&second, -native_ov000_data_022385b8.field18);
    native_fn_02028044(&third, native_ov000_data_022385b8.field14);
    native_fn_02000e1c(&second, &third, &first);
    actor->transformed.v[0] = 0;
    actor->transformed.v[1] = 0;
    actor->transformed.v[2] = native_ov000_data_022385b8.field10;
    native_fn_0200103c(&actor->transformed, &first, &actor->transformed);
}
