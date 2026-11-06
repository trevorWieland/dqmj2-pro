#include "context.h"
int native_main_02098f48(DWCHttp*http,char*label,char*buffer,int size){char*value=native_fn_02098ed8(http,label);if(!value)return 0;if((int)native_fn_0201d69c(value)>=size)return 0;native_fn_0201d6b8(buffer,value);return 1;}
