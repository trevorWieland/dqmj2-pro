#include "context_00.h"
void native_main_020387a8 (NNSSndSeqPlayer * seqPlayer)
{
    NNSSndPlayer * player;
    ((void) 0) ;
    if (seqPlayer->handle != ((void *)0) ) {
        ((void) 0) ;
        seqPlayer->handle->player = ((void *)0) ;
        seqPlayer->handle = ((void *)0) ;
    }
    player = seqPlayer->player;
    ((void) 0) ;
    native_fn_0202bb28(&player->playerList, seqPlayer);
    seqPlayer->player = ((void *)0) ;
    if (seqPlayer->heap != ((void *)0) ) {
        native_fn_0202ba20(&player->heapList, seqPlayer->heap);
        seqPlayer->heap->player = ((void *)0) ;
        seqPlayer->heap = ((void *)0) ;
    }
    native_fn_0202bb28(&native_data_main_020f4360.field_000c, seqPlayer);
    native_fn_0202ba20(&native_data_main_020f4360.field_0000, seqPlayer);
    seqPlayer->status = NNS_SND_SEQ_PLAYER_STATUS_STOP;
}
