#include "context.h"
u8 native_main_020956dc(void)
{
 ACWORK*wk=DWCi_AC_GetMemPtr(16);
 u8 result=9;
 int phase=WCM_GetPhase();
 switch(phase){
 case 0:break;
 case 1:break;
 case 2:break;
 case 3:
  result=wk->phaseBak;
  if(wk->duplicateFlag==1){wk->findList[wk->connectNo].state=0;result=7;}
  else if(result>=3&&result<=5)DWCi_AC_SearchReStart(result);
  break;
 case 4:break;
 case 5:break;
 case 6:WCM_EndSearchAsync();break;
 case 7:break;
 case 8:break;
 case 9:WCM_DisconnectAsync();break;
 case 10:break;
 case 12:WCM_TerminateAsync();DWCi_AC_SetError(4);result=17;break;
 case 11:DWCi_AC_SetError(0);result=17;
 }
 return result;
}
