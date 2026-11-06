#include "stride_words.h"

u32 native_main_0209b438(const u16 *value) {
    const u16 *cursor;
    u32 count;
    cursor=value;
    count=0;
    if (*cursor!=0) {
        do {
            cursor+=1;
            count+=1;
        } while (*cursor!=0);
    }
    return count;
}
