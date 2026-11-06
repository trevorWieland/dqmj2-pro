#include "context000.h"

int native_main_020211e8(wchar_t *text,size_t capacity,const wchar_t *format,va_list arguments)
{
    int count;
    Output output;
    output.text=text;
    output.capacity=capacity;
    output.written=0;
    count=native_fn_02020890(native_fn_02021180,&output,format,arguments);
    if (count<0) return count;
    if ((unsigned int)count<capacity) {text[count]=0;return count;}
    (text+capacity)[-1]=0;
    return -1;
}
