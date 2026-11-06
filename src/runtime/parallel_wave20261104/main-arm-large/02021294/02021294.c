#include "context000.h"

wchar_t *native_main_02021294(wchar_t *dest,const wchar_t *source)
{
    wchar_t *p=dest;
    while (*p++);
    --p;
    while (*p++ =*source++);
    return dest;
}
