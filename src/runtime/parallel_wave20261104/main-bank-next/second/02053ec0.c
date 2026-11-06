#include "context.h"
void native_main_02053ec0(Context *context, const Instruction *instruction)
{
    int index = 0;
    do {
        native_fn_0205bd60()[index] = -1;
        ++index;
    } while (index < 3);
    context->records[context->bank].position += instruction->advance;
    context->records[context->bank].status = 0;
}
