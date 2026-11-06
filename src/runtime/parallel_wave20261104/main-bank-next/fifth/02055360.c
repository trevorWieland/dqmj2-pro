#include "context.h"
void native_main_02055360(Context *context, const Instruction *instruction, int selector)
{
    float first = context->parameters[0];
    float second = context->parameters[1];
    float third = context->parameters[2];
    const int *coordinates = native_fn_ov000_021e6a40(selector, 0);
    context->parameters[0] = (float)coordinates[0] / 4096.0f;
    context->parameters[1] = (float)coordinates[1] / 4096.0f;
    context->parameters[2] = (float)coordinates[2] / 4096.0f;
    native_fn_ov000_021e70b0(selector, TO_FIXED(first), TO_FIXED(second), TO_FIXED(third));
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
