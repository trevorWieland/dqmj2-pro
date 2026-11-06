#include "context.h"
int native_main_020952d0(int error)
{
  int iVar1;
  
  switch(error) {
  case AC_ERROR_WCM_START_UP:
    iVar1 = DWC_AC_STATE_ERROR_START_UP;
    break;
  case AC_ERROR_WCM_FATAL:
    iVar1 = DWC_AC_STATE_ERROR_FATAL;
    break;
  case AC_ERROR_SOC_START_UP:
    iVar1 = DWC_AC_STATE_ERROR_SOCKET_START;
    break;
  case AC_ERROR_NETCHECK_CREATE:
    iVar1 = DWC_AC_STATE_ERROR_NETCHECK_CREATE;
    break;
  default:
    iVar1 = 0;
  }
  return iVar1;
}
