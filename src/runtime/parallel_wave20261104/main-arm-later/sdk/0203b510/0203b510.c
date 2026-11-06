#include "context000.h"

void native_main_0203b510 (void * arg)
{
    NNSSndStrmThread * thread = (NNSSndStrmThread *)arg;
    while (1) {
        LoadCommand * command;
        native_fn_020068d4(&thread->threadQ);
        while (1) {
            native_fn_0200708c(&thread->mutex);
            command = native_fn_0203a77c(&thread->commandList);
            if (command == ((void *)0) ) {
                native_fn_02007110(&thread->mutex);
                break;
            }
            native_fn_0203ab50(command);
            native_fn_0203a80c(command);
            native_fn_02007110(&thread->mutex);
        }
    }
}
