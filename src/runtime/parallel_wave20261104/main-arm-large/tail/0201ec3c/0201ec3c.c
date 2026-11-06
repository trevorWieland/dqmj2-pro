#include "context000.h"

double native_main_0201ec3c(const char *str,char **end)
{
    double value,magnitude;
    int count,overflow;
    Reader reader;
    reader.next=str;
    reader.null_seen=0;
    value=native_fn_0201d9f0(2147483647,native_fn_0201d618,&reader,&count,&overflow);
    if (end) *end=(char *)str+count;
    magnitude=native_fn_02022664(value);
    if (overflow || (value!=0.0 && (magnitude<2.2250738585072014e-308 || magnitude>1.7976931348623157e308))) native_data_020ec9b0=34;
    return value;
}
