#include "context.h"
int native_main_02098a7c(DWCHttp*http,DWCHttpBuffer*buf,int len){DWCAuthAlloc alloc=http->param.alloc;if(len==0)return 0;buf->buffer=alloc((unsigned long)native_data_020deec4,len);if(!buf->buffer)return 0;buf->write_index=buf->buffer;buf->length=len;buf->buffer_tail=buf->buffer+len;return 1;}
