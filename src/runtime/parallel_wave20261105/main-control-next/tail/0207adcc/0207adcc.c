#include "context000.h"

int native_main_0207adcc(int index,int level,int code){
    const Info *info;
    int result=0;
    int i;
    const Item *item;
    info=native_fn_0207aa98(index);
    item=info->items;
    for(i=0;i<10;++i,++item){
        if(info->results[i]!=0 && level>=*(const u8 *)((unsigned int)info+i) && code==item->code){result=info->results[i];break;}
    }
    return result;
}
