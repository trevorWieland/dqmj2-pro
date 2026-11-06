#include "context_00.h"
void native_main_020382fc (void)
{
    NNSSndSeqPlayer * seqPlayer;
    NNSSndSeqPlayer * next;
    u32 status;
    int fader;
    status = native_fn_02009ce8();
    for (seqPlayer = (NNSSndSeqPlayer *)native_fn_0202bb88(&native_data_main_020f4360.field_000c, ((void *)0) );
         seqPlayer != ((void *)0) ; seqPlayer = next) {
        next = (NNSSndSeqPlayer *)native_fn_0202bb88(&native_data_main_020f4360.field_000c, seqPlayer);
        if (!seqPlayer->startFlag) {
            if (native_fn_02009a0c(seqPlayer->commandTag)) {
                seqPlayer->startFlag = 1 ;
            }
        }
        if (seqPlayer->startFlag) {
            if ((status & (1 << seqPlayer->playerNo)) == 0) {
                native_fn_020387a8(seqPlayer);
                continue;
            }
        }
        native_fn_02037a20(&seqPlayer->fader);
        fader
            = SND_CalcDecibel(seqPlayer->initVolume)
              + SND_CalcDecibel(seqPlayer->extVolume)
              + SND_CalcDecibel(seqPlayer->player->volume)
              + SND_CalcDecibel(native_fn_020379ec(&seqPlayer->fader) >> 8 )
            ;
        if (fader < -32768) fader = -32768;
        else if (fader > 32767) fader = 32767;
        if (fader != seqPlayer->volume) {
            native_fn_02009148(seqPlayer->playerNo, fader);
            seqPlayer->volume = (s16)fader;
        }
        if (seqPlayer->status == NNS_SND_SEQ_PLAYER_STATUS_FADEOUT) {
            if (native_fn_02037a38(&seqPlayer->fader)) {
                native_fn_02038708(seqPlayer);
            }
        }
        if (seqPlayer->prepareFlag) {
            native_fn_02009108(seqPlayer->playerNo);
            seqPlayer->prepareFlag = 0 ;
        }
    }
}
