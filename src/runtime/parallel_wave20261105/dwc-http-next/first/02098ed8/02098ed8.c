#include "context.h"
char*native_main_02098ed8(DWCHttp*http,char*label){int i;for(i=0;i<32;i++){if(!http->labelvalue[i].label)break;if(!native_fn_0201d800(label,http->labelvalue[i].label))return http->labelvalue[i].value;}return NULL;}
