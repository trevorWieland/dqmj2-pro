#include "context.h"
void native_main_0205443c(Context *context, const Instruction *instruction)
{
    int apply = (int)context->parameters[0];
    const Vec3 *point = ov000_saved_world_position_get_021e07b8(0);
    SceneState *state = native_fn_ov000_021e07ac();
    Vec3 result;
    if (native_fn_ov000_021da5e4(point, state->matrix, &result, 1) && apply) {
        native_fn_ov000_021dbbb8(state->matrix, &result);
        state->position.x = result.x;
        state->position.y = result.y;
        state->position.z = result.z;
    }
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
