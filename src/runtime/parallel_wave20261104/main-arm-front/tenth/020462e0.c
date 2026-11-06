#include "context.h"
void native_main_020462e0(s32 index,u32 screen,u32 tile) {
    Config *config=&native_data_main_020faaec[index];
    u8 mode;
    native_data_main_020fab2c[index].value=screen;
    native_data_main_020fab30[index].value=tile;
    mode=native_fn_02087544(index)?0:1;
    native_fn_0204535c(mode,(u8)screen,config->source0,tile<<5,config->bytes8);
    if(config->palette4) {
        if(native_fn_02087544(index))native_fn_020481b8(config->palette4,128,config->paletteBytesC);
        else native_fn_0204820c(config->palette4,128,config->paletteBytesC);
    }
}
