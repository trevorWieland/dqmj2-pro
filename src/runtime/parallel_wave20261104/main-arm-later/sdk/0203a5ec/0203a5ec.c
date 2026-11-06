#include "context000.h"

void native_main_0203a5ec (NNSSndStrmPlayer * player)
{
    ((void) 0) ;
    if (!player->activeFlag) return;
    native_fn_0203a688(player);
    player->closeStreamFunc(player);
    native_fn_0203a70c(&native_data_020f5040.commandList, player);
    if (native_data_020f4c84.prepareThread) native_fn_0203a70c(&native_data_020f4c84.prepareThread->commandList, player);
    native_fn_0203a260(player);
}

#include "context001.h"
