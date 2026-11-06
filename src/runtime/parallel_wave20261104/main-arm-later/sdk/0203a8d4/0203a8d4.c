#include "context000.h"

void native_main_0203a8d4 (NNSSndStrmCallbackStatus status, int numChannels, void * buffer[], u32 len, NNSSndStrmFormat, void * arg)
{
    NNSSndStrmPlayer * player = (NNSSndStrmPlayer *)arg;
    LoadCommand * command;
    NNSSndStrmThread * thread;
    int ch;
    ((void) 0) ;
    if (player->commandCount >= 4 - 2) {
        command = ((void *)0) ;
        while ((command = (LoadCommand *)native_fn_0202bb88(&native_data_020f5040.commandList, command)) != ((void *)0) ) {
            if (command->player == player) break;
        }
        ((void) 0) ;
        for (ch = 0; ch < command->numChannels; ch++) {
            MI_CpuClear8(command->buffer[ ch ], command->bufLen);
        }
        native_fn_0202bb28(&native_data_020f5040.commandList, command);
        player->commandCount--;
        native_fn_0203a80c(command);
    }
    command = native_fn_0203a7cc();
    ((void) 0) ;
    command->player = player;
    command->status = status;
    command->numChannels = numChannels;
    for (ch = 0; ch < numChannels; ch++) {
        command->buffer[ ch ] = buffer[ ch ];
    }
    command->bufLen = len;
    thread = &native_data_020f5040;
    if (status == NNS_SND_STRM_CALLBACK_SETUP && native_data_020f4c84.prepareThread) thread = native_data_020f4c84.prepareThread;
    player->commandCount++;
    native_fn_0202ba20(&thread->commandList, command);
    native_fn_02006924(&thread->threadQ);
}
