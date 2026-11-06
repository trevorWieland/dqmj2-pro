#include "context_00.h"
BOOL native_main_02039ba0 (NNSSndHandle * handle, int playerNo, int bankNo, int playerPrio, const NNSSndArcSeqInfo * info, int seqNo)
{
    NNSSndSeqPlayer * player;
    NNSSndHeapHandle heap;
    NNSSndSeqData * seq;
    SNDBankData * bank;
    NNSSndArcLoadResult result;
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
    result = native_fn_02039208(seqNo, (1 << 0) , heap, 0 , &seq);
    if (result != NNS_SND_ARC_LOAD_SUCESS) {
        native_fn_020384f8(player);
        return 0 ;
    }
    native_fn_02038504(
        player,
        (u8 *)seq + seq->baseOffset,
        0,
        bank
        );
    native_fn_02038134(handle, info->param.volume);
    native_fn_02038174(handle, info->param.channelPrio);
    native_fn_020381d4(handle, seqNo);
    return 1 ;
}
