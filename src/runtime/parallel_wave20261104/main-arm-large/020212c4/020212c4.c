#include "context000.h"

wchar_t *native_main_020212c4(const wchar_t *str,wchar_t chr)
{
 wchar_t ch;
 while((ch=*str++)!=0) {if(ch==chr)return (wchar_t*)str-1;}
 return chr?0:(wchar_t*)str-1;
}
