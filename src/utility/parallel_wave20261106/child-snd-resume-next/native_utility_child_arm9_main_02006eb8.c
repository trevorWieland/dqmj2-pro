#include "context.h"
BOOL native_utility_child_arm9_main_02006eb8 (NNSSndHandle * handle, int playerNo, int bankNo, int playerPrio, const NNSSndSeqArcSeqInfo * sound, const NNSSndSeqArc * seqArc, int seqArcNo, int index)
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
    player = native_fn_utility_child_arm9_main_02005884(handle, playerNo, playerPrio);
    if (player == ((void *)0) ) return 0 ;
    heap = native_fn_utility_child_arm9_main_0200577c(playerNo, player);
    result = native_fn_utility_child_arm9_main_02006d70(bankNo, (1 << 1) | (1 << 2) , heap, 0 , &bank);
    if (result != NNS_SND_ARC_LOAD_SUCESS) {
        native_fn_utility_child_arm9_main_02005878(player);
        return 0 ;
    }
    native_fn_utility_child_arm9_main_02005820(
        player,
        (u8 *)seqArc + seqArc->baseOffset,
        sound->offset,
        bank
        );
    native_fn_utility_child_arm9_main_02005bb4(handle, sound->param.volume);
    native_fn_utility_child_arm9_main_02005b8c(handle, sound->param.channelPrio);
    native_fn_utility_child_arm9_main_02005b64(handle, seqArcNo, index);
    return 1 ;
}
