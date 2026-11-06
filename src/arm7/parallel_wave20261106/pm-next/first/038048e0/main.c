#include "context.h"
void native_host_arm7_wram_038048e0(u32 data)
{
 if(data&0x02000000){int i;for(i=0;i<16;i++)native_host_arm7_command_words_03809eb0[i]=0;}
 native_host_arm7_command_words_03809eb0[(data&0xf0000)>>16]=(u16)data;
 if(data&0x01000000){
  u16 command=(native_host_arm7_data_03809eac.command[0]&0xff00)>>8;
  switch(command){
   case 0x60:
    while(native_host_arm7_arm_037fe410(8,0x0300e000,0)<0){}
    break;
   case 0x62:
    if(!native_host_arm7_arm_03803b7c(3,command,2,native_host_arm7_data_03809eac.command[0]&255,native_host_arm7_data_03809eac.command[1]))native_host_arm7_wram_03804b80(command,65535,1);
    break;
   case 0x61:
    if(!native_host_arm7_arm_03803b7c(3,command,2,native_host_arm7_data_03809eac.command[0]&255,native_host_arm7_data_03809eac.command[1]))native_host_arm7_wram_03804b80(command,65535,1);
    break;
   default:native_host_arm7_wram_03804b80(command,1,0);break;
  }
 }
}
