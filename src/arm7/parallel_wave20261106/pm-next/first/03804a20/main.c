#include "context.h"
typedef struct ServiceEntry {u32 device,command,args[4];} ServiceEntry;
void native_host_arm7_wram_03804a20(void *message)
{
 ServiceEntry *entry=message;
 u32 state=native_host_arm7_arm_037fdd00();
 if(!native_host_arm7_arm_03803b0c(3)){
  native_host_arm7_arm_037fdd14(state);
  native_host_arm7_wram_03804b80((u16)entry->command,65535,1);
  return;
 }
 native_host_arm7_arm_03803b28(3);
 native_host_arm7_arm_037fdd14(state);
 switch(entry->command){
  case 0x62:
   while(native_host_arm7_arm_037fe410(8,0x0300e200,0)<0){}
   native_host_arm7_data_03809eac.status=1;
   native_host_arm7_arm_03804fbc(entry->args[0]&31,entry->args[1],entry->args[0]&0xc0);
   break;
  case 0x61:{
   u32 operation,value,result;
   native_host_arm7_data_03809eac.status=2;
   operation=entry->args[0];value=entry->args[1];
   if(operation==14){while(native_host_arm7_arm_037fe410(8,0x0300e100,0)<0){}}
   result=native_host_arm7_arm_03804d40(operation,(u16)value);
   native_host_arm7_wram_03804b80(0x61,result,0);
   break;
  }
  case 0x64:native_host_arm7_arm_03804f54(entry->args[0]);break;
  default:native_host_arm7_wram_03804b80((u16)entry->command,1,0);break;
 }
 native_host_arm7_arm_03803b40(3);
}
