#include "context.h"
void native_main_0204dae0(ExtendedContext *context,const Instruction *instruction)
{
    if(ORIGINAL_COMMAND_FLAG) {
        ExtendedRecord *record=&context->records[context->bank];
        if(record->field8==0) {
            if(native_fn_ov000_0221a028()) {native_fn_ov000_02219fd8(8);record->field8=1;}
            else record->field8=10;
        }
        if(record->field8==1 && !native_fn_ov000_0221a010()) record->field8=2;
        if(record->field8==2) {native_fn_ov000_02219ed8();native_fn_ov000_02219e14();record->field8=10;}
        if(record->field8==10) {
            record->field8=0;ORIGINAL_COMMAND_FLAG=0;
            context->records[context->bank].position+=instruction->advance;
        }
    } else context->records[context->bank].position+=instruction->advance;
    context->records[context->bank].status=1;
}
