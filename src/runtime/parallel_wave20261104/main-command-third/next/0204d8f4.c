#include "context.h"
void native_main_0204d8f4(ExtendedContext *context,const Instruction *instruction)
{
    if(ORIGINAL_COMMAND_FLAG && native_fn_ov000_0221a028()) {
        native_fn_ov000_0221a080(instruction->payload);
        native_fn_ov000_02219fd8(7);
        native_fn_ov000_0221a0bc(0);
        context->records[context->bank].position+=instruction->advance;
    }
    context->records[context->bank].status=1;
}
