#include "context.h"
void native_main_020990f0(void)
{
  if(DWCnetcheck != NULL) {
    DWC_Printf(DWC_REPORTFLAG_AUTH, "Netcheck : Aborting\n");
    if(DWChttp != NULL) {
      DWC_Printf(DWC_REPORTFLAG_AUTH, "Netcheck : Http abort\n");
      native_fn_020983d0(DWChttp);
      DWC_Printf(DWC_REPORTFLAG_AUTH, "Netcheck : Http abort finished\n");
    }
    DWC_Printf(DWC_REPORTFLAG_AUTH,"Netcheck : Auth abort\n");
    native_fn_020975b8();
    DWC_Printf(DWC_REPORTFLAG_AUTH,"Netcheck : Auth abort finished\n");
    if ((DWCnetcheck->thread).id != 0) {
      native_fn_02006890(&DWCnetcheck->thread);
    }
    DWCnetcheck->returncode = -7;
    DWC_Printf(DWC_REPORTFLAG_AUTH,"Netcheck : Aborted\n");
  }
  return;
}
