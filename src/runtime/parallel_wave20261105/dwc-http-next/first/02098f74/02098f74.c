#include "context.h"
void native_main_02098f74(DWCHttp*http,DWCHttpLabelValue*entries,int count){DWCAuthFree free=http->param.free;int i;for(i=0;i<count;i++){if(entries[i].label){free((u32)native_data_020defb0,entries[i].label,0);entries[i].label=NULL;}if(entries[i].value){free((u32)native_data_020defcc,entries[i].value,0);entries[i].value=NULL;}}}
