#include "context.h"
u32 native_main_02042aac(Object *object) {
    s32 frame;
    u32 result;
    s32 position;
    Entry *entry;
    frame=*object->pointer60>>12;
    result=0;
    position=0;
    object->byte1dc=-1;
    do {
        entry=native_fn_02042d58(object->word164,frame,&position);
        if(!entry)break;
        if(entry->word2==2 && (s32)entry->word4>=0) {
            if(object->byte1df)object->byte1dc=native_fn_0205e7a8(0xffffffff,entry->word4);
            result|=4;
        }
    }while(position>=0);
    return result;
}
