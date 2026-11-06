#include "context.h"
void native_main_02056390(Context *context, const Instruction *instruction)
{
    int object = (int)context->parameters[0];
    int other = (int)context->parameters[1];
    int coordinates[3];
    native_fn_ov000_021f3e5c(object, coordinates);
    context->parameters[0] = (float)coordinates[0] / 4096.0f;
    context->parameters[1] = (float)coordinates[1] / 4096.0f;
    context->parameters[2] = (float)coordinates[2] / 4096.0f;
    context->parameters[3] = (float)native_fn_ov000_021f3f68(object) / 4096.0f;
    native_fn_ov000_021f3dac(object, other);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
