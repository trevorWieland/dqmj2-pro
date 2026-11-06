#include "context.h"
u32 native_main_020470fc(const u16 *text) {
    u32 result=0;
    if(text) {
        u16 index=0;
        do {
            if(!text[index]) {result=index;break;}
            index++;
        }while(index<512);
    }
    return result;
}
