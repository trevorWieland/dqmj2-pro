#include "context.h"
int native_main_020b9868(const char*name){int length,i;if(name){length=native_fn_02019d80(name);if(length>2&&length<=64){length--;for(i=1;i<length;i++){if(name[i]==46)return 1;}}}return 0;}
