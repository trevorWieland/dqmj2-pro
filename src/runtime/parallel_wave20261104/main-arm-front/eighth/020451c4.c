#include "context.h"
void *native_main_020451c4(const char *path,u32 index,u32 heap,s32 *size) {
    FSFile file;
    u32 count;
    u32 start;
    u32 end;
    s32 bytes;
    void *result=0;
    native_data_main_020f6a08=0;
    if(heap==0xffffffff)heap=native_fn_0202a250();
    native_fn_0200bd04(&file);
    if(native_fn_0200bfe4(&file,path)) {
        native_fn_0200c180(&file,&count,4);
        if(count<=index)native_fn_02008430();
        native_fn_0200c190(&file,index*4+4,0);
        native_fn_0200c180(&file,&start,4);
        native_fn_0200c180(&file,&end,4);
        if((s32)end<(s32)start)native_fn_02008430();
        if(size && *size)bytes=*size;
        else {bytes=end-start;if(size)*size=bytes;}
        result=native_fn_0202a37c(heap,(bytes+3)&~3,4);
        native_fn_0200c190(&file,start,0);
        if(native_fn_0200c180(&file,result,bytes)<=0)native_data_main_020f6a08=1;
        else {native_fn_02007308(result,bytes);native_data_main_020f6a08=0;}
        native_fn_0200c02c(&file);
    } else native_data_main_020f6a08=2;
    return result;
}
