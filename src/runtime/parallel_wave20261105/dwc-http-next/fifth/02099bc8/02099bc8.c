#include "context.h"
void native_main_02099bc8(DWCNetcheckError aErr)
{
  native_fn_0200708c(&DWCnetcheck->mutex);
  DWCnetcheck->error = aErr;
  native_fn_02007110(&DWCnetcheck->mutex);
  return;
}
