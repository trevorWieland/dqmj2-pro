#include "context000.h"

void native_main_0203aa0c (NNSSndStrmPlayer * player)
{
    NNSSndArcStrmCallbackInfo info;
    NNSSndArcStrmCallbackParam param;
    const NNSSndArcStrmInfo * strmInfo;
    u8 old_format;
    u16 old_sampleRate;
    u64 tmpU64;
    BOOL result;
    info.playerNo = player->playerNo;
    info.strmNo = player->strmNo;
    param.strmNo = player->strmNo;
    param.offset = 0;
    result = player->sndArcStrmCallback(
        NNS_SND_ARC_STRM_CALLBACK_DATA_END,
        &info,
        &param,
        player->sndArcStrmCallbackArg
        );
    if (!result) return;
    strmInfo = native_fn_02038f18(param.strmNo);
    if (strmInfo == ((void *)0) ) return;
    old_format = player->info.format;
    old_sampleRate = player->info.sampleRate;
    player->closeStreamFunc(player);
    native_fn_0203b378(player, strmInfo->fileId);
    if (!player->openStreamFunc(player, strmInfo->fileId)) {
        return;
    }
    if (old_sampleRate != player->info.sampleRate) {
        ((void)0)
            ;
        return;
    }
    if (old_format == STRM_FORMAT_PCM8 && player->info.format != STRM_FORMAT_PCM8 ||
        old_format != STRM_FORMAT_PCM8 && player->info.format == STRM_FORMAT_PCM8) {
        ((void)0) ;
        return;
    }
    player->strmNo = param.strmNo;
    tmpU64 = player->info.sampleRate;
    tmpU64 *= param.offset;
    tmpU64 /= 1000;
    player->curSample = (u32)tmpU64;
    if (player->curSample != 0 && player->info.format == STRM_FORMAT_ADPCM) {
        player->dirtyFlag = 1 ;
    } else {
        player->dirtyFlag = 0 ;
    }
    player->finishFlag = 0 ;
}

#include "context001.h"
