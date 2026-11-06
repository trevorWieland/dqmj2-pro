#include "context.h"
void native_main_02099dc8(void)
{
  if (native_data_021d19a4 != NULL) {
    native_fn_020987b0(&native_data_021d19a4->http);
    (*native_data_021d19a4->free)((int)native_data_020df22c,native_data_021d19a4,0);
    native_data_021d19a4 = NULL;
  }
  return;
}
