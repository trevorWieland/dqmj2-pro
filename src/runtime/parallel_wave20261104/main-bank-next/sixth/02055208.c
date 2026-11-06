#include "context.h"
void native_main_02055208(Context *context, const Instruction *instruction, int selector)
{
    int first = (int)context->parameters[0];
    const int *coordinates = native_fn_ov000_021e6a40(selector, 0);
    context->parameters[0] = (float)coordinates[0] / 4096.0f;
    context->parameters[1] = (float)coordinates[1] / 4096.0f;
    context->parameters[2] = (float)coordinates[2] / 4096.0f;
    native_fn_ov000_021e6b64(selector, first);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
