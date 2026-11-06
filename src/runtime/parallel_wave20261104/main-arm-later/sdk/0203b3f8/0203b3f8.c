#include "context000.h"

BOOL native_main_0203b3f8 (NNSSndStrmPlayer * player, u32 fileId)
{
    if (native_fn_02039094(fileId, &player->info, sizeof(player->info), 0) != sizeof(player->info)) {
        return 0 ;
    }
    if (!native_fn_0200bf74(&player->file, native_fn_0203915c())) {
        return 0 ;
    }
    player->fileOffset = native_fn_02039044(fileId);
    return 1 ;
}
