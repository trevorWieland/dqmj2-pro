#include "context.h"
int native_main_0208ec60(PipeView *pipe,CommandHeader *command)
{
    int result;
    if(command->blockD==1){
        void *response;
        MessageQueue queue;
        native_fn_02006dfc(&queue,&response,1);
        command->response8=&queue;
        (void)native_fn_0208ec1c(pipe,command);
        (void)native_fn_02006eb8(&queue,(void **)&result,1);
    }else{
        command->response8=0;
        result=native_fn_0208ec1c(pipe,command);
    }
    return result;
}
