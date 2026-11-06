#include "context.h"
void native_main_02055c90(Context *context, const Instruction *instruction)
{
    int object = (int)context->parameters[0];
    float first = context->parameters[1];
    float second = context->parameters[2];
    float third = context->parameters[3];
    int coordinates[3];
    native_fn_ov000_021f3e5c(object, coordinates);
    context->parameters[0] = (float)coordinates[0] / 4096.0f;
    context->parameters[1] = (float)coordinates[1] / 4096.0f;
    context->parameters[2] = (float)coordinates[2] / 4096.0f;
    coordinates[0] = TO_FIXED(first);
    coordinates[1] = TO_FIXED(second);
    coordinates[2] = TO_FIXED(third);
    native_fn_ov000_021f3e88(object, coordinates[0], coordinates[1], coordinates[2]);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
