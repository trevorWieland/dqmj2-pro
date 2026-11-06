#include "context.h"
double native_main_020a6090(Server *server,const char *key,double fallback)
{
 const char *s=native_fn_020a5fe4(server,key,0);
 if(s==0)return fallback;
 return native_fn_0201ed1c(s);
}
