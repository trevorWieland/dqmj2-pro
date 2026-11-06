#include "context.h"
void native_main_02055020(Context *context, const Instruction *instruction)
{
    u32 first = native_fn_0205be14();
    int second = native_fn_0205be64();
    context->parameters[0] = (float)first;
    context->parameters[1] = (float)second;
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
