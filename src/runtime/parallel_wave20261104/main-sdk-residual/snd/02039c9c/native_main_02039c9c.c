#include "context_00.h"
BOOL native_main_02039c9c (NNSSndHandle * handle, int playerNo, int bankNo, int playerPrio, const NNSSndSeqArcSeqInfo * sound, const NNSSndSeqArc * seqArc, int seqArcNo, int index)
{
    NNSSndSeqPlayer * player;
    NNSSndHeapHandle heap;
    SNDBankData * bank;
    NNSSndArcLoadResult result;
    ((void) 0) ;
    ((void) 0) ;
    ((void) 0) ;
    ((void) 0) ;
    ((void) 0) ;
    player = native_fn_02038460(handle, playerNo, playerPrio);
    if (player == ((void *)0) ) return 0 ;
    heap = native_fn_020385c8(playerNo, player);
    result = native_fn_0203928c(bankNo, (1 << 1) | (1 << 2) , heap, 0 , &bank);
    if (result != NNS_SND_ARC_LOAD_SUCESS) {
        native_fn_020384f8(player);
        return 0 ;
    }
    native_fn_02038504(
        player,
        (u8 *)seqArc + seqArc->baseOffset,
        sound->offset,
        bank
        );
    native_fn_02038134(handle, sound->param.volume);
    native_fn_02038174(handle, sound->param.channelPrio);
    native_fn_020381f8(handle, seqArcNo, index);
    return 1 ;
}
