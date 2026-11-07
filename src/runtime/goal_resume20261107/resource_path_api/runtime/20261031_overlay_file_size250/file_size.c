#include "context.h"
unsigned int native_main_0202a8e0(const void *path)
{
    FSFile file;
    unsigned int length=0;
    native_fn_0200bd04(&file);
    if(native_fn_0200bfe4(&file,path)){
        length=file.prop.file.bottom-file.prop.file.top;
        native_data_020edec8=length!=0?0:3;
        native_fn_0200c02c(&file);
    }else native_data_020edec8=1;
    return length;
}
