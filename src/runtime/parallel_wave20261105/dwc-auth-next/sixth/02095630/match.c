#include "context.h"
u8 native_main_02095630(tagACWORK*work)
{
 u8 count=0;
 int i;
 for(i=0;i<work->findListNum;i++){
  if(work->findList[i].state==0&&work->bssDesc[i].channel-1!=work->findList[i].channel){
   work->findList[i].find=0;
   count++;
  }else work->findList[i].find=1;
 }
 return count;
}
