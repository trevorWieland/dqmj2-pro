#include "context.h"
int native_main_0208ec1c(PipeView *pipe,CommandHeader *command)
{
    s32 result;
    s32 block;
    block=(command && !(command->blockD&1))?0:1;
    result=native_fn_02006e24(&pipe->queue0,command,block);
    if(!result)native_fn_0208ebfc(command);
    return result?0:-42;
}
