#include "context_00.h"
NNSSndSeqPlayer * native_main_02038460 (NNSSndHandle * handle, int playerNo, int prio)
{
    NNSSndSeqPlayer * seqPlayer;
    NNSSndPlayer * player;
    ((void) 0) ;
    ((void) 0) ;
    ((void) 0) ;
    player = &native_data_main_020f4360.field_0458[ playerNo ];
    if (NNS_SndHandleIsValid(handle)) {
        native_fn_02038100(handle);
    }
    if (player->playerList.numObjects >= player->playableSeqCount) {
        seqPlayer = (NNSSndSeqPlayer *)native_fn_0202bb88(&player->playerList, ((void *)0) );
        if (seqPlayer == ((void *)0) ) return ((void *)0) ;
        if (prio < seqPlayer->prio) return ((void *)0) ;
        native_fn_02038708(seqPlayer);
    }
    seqPlayer = native_fn_02038740(prio);
    if (seqPlayer == ((void *)0) ) return ((void *)0) ;
    native_fn_02038664(player, seqPlayer);
    seqPlayer->handle = handle;
    handle->player = seqPlayer;
    return seqPlayer;
}
