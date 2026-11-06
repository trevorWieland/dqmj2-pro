#include "context.h"
void native_main_0208eccc(PipeView *pipe)
{
    CommandHeader *command;
    u32 level;
    int result;
    for(;;){
        (void)native_fn_02006ff8(&pipe->queue0,(void **)&command,1);
        if(!command)break;
        result=command->handler0(command);
        level=native_fn_02007ff4();
        (void)native_fn_02006c70();
        (void)native_fn_02006eb8(&pipe->queue0,0,0);
        if(command->socket4)((ResultSocket *)command->socket4)->result6C=result;
        if(command->response8)(void)native_fn_02006e24(command->response8,(void *)result,0);
        native_fn_0208ebfc(command);
        (void)native_fn_02006ca4();
        native_fn_02008008(level);
    }
}
