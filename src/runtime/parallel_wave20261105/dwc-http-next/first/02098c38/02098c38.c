#include "context.h"
int native_main_02098c38(DWCHttp * aHttp,  DWCHttpParseResult *aResult, char *aLabel, char *aContent)
{
  DWCAuthAlloc alloc=aHttp->param.alloc;DWCAuthFree free=aHttp->param.free;size_t sVar1;
  undefined4 uVar2;
  u8 * labelBuf;
  u8 * valueBuf;
  if(aResult->index>aResult->len)return 0;
    sVar1 = native_fn_0201d69c(aLabel);
    labelBuf = alloc((int)native_data_020def18, sVar1 + 1);
    aResult->entry[aResult->index].label = labelBuf;
    if(aResult->entry[aResult->index].label != NULL){
      sVar1 = native_fn_0201d69c(aContent);
     valueBuf = alloc((int)native_data_020def38, sVar1 + 1);
      aResult->entry[aResult->index].value = valueBuf;
      if (aResult->entry[aResult->index].value != NULL) {
        native_fn_0201d6b8(aResult->entry[aResult->index].label, aLabel);
        native_fn_0201d6b8(aResult->entry[aResult->index].value, aContent);
        aResult->index = aResult->index + 1;
        return 1;
      }
    }
    DWC_Printf(DWC_REPORTFLAG_AUTH, "\t\tHttp : failed to add result\n");
    if (aResult->entry[aResult->index].label != NULL) {
      free((int)native_data_020def58, aResult->entry[aResult->index].label, 0);
      aResult->entry[aResult->index].label = NULL;
    }
    if (aResult->entry[aResult->index].value != NULL) {
      free((int)native_data_020def74, aResult->entry[aResult->index].value, 0);
      aResult->entry[aResult->index].value = NULL;
    }
  return 0;
}
