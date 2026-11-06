#include "context.h"
void native_main_020574a4(Context *context, const Instruction *instruction)
{
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
