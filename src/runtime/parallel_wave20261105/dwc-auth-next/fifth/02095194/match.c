#include "context.h"
u32 native_main_02095194(u8 *param_1)
{
  int iVar1;
  
  if (*param_1 <= 10) {
    iVar1 = native_fn_020951e4();
    if (iVar1 == 1) {
      *param_1 = 0;
      return 1;
    }
    if (iVar1 == -1) {
      *param_1 = 0x12;
      return 1;
    }
  }
  else if (*param_1 == 0xe) {
    native_fn_020990f0();
    native_fn_02099058();
    *param_1 = 0xc;
  }
  else if ((*param_1 < 0x12) && (iVar1 = native_fn_02095248(), iVar1 == 1)) {
    *param_1 = 10;
  }
  return 0;
}
