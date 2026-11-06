#include "context.h"
void native_main_0204dbe8(ExtendedContext *context,const Instruction *instruction)
{
    if(ORIGINAL_COMMAND_FLAG) {
        if(native_fn_ov000_0221a028()) {
            ExtendedRecord *record=&context->records[context->bank];
            if(record->field8==0) {if(native_fn_ov000_0221a064())record->field8=1;}
            else if(record->field8==1 && !native_fn_ov000_0221a064()) {
                record->field8=0;
                context->records[context->bank].position+=instruction->advance;
            }
        }
    } else if(native_fn_0202a634()->field2&1)context->records[context->bank].position+=instruction->advance;
    context->records[context->bank].status=1;
}
