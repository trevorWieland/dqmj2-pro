#include "context.h"
u32 native_host_arm7_wram_03804d40(u32 operation,u16 value)
{
 switch(operation){
  case 1:native_host_arm7_arm_0380528c(1);native_host_arm7_arm_03804f54(1);break;
  case 2:native_host_arm7_arm_0380528c(3);native_host_arm7_arm_03804f54(3);break;
  case 3:native_host_arm7_arm_0380528c(2);native_host_arm7_arm_03804f54(2);break;
  case 4:native_host_arm7_arm_03804cf0(4);break;
  case 5:native_host_arm7_arm_03804d14(4);break;
  case 6:native_host_arm7_arm_03804cf0(8);break;
  case 7:native_host_arm7_arm_03804d14(8);break;
  case 8:native_host_arm7_arm_03804cf0(12);break;
  case 9:native_host_arm7_arm_03804d14(12);break;
  case 10:native_host_arm7_arm_03804cf0(1);break;
  case 11:native_host_arm7_arm_03804d14(1);break;
  case 12:native_host_arm7_arm_03804d14(2);break;
  case 13:native_host_arm7_arm_03804cf0(2);break;
  case 14:native_host_arm7_arm_037fe708();native_host_arm7_arm_03804cf0(64);break;
  case 15:
   switch(value){
    case 0:return native_host_arm7_arm_03804c7c(1)&1;
    case 1:return native_host_arm7_arm_03804c7c(0)&12;
    case 2:return native_host_arm7_arm_03804c7c(0)&1;
    case 3:return 0;
    case 4:return native_host_arm7_arm_03804c7c(2)&1;
    case 5:return native_host_arm7_arm_03804c7c(3)&3;
    case 6:return(u16)native_host_arm7_arm_038052a8();
    default:return 2;
   }
  case 16:native_host_arm7_arm_03804c00(2,value&1);break;
  case 17:native_host_arm7_arm_03804c00(3,value&3);break;
  case 18:native_host_arm7_arm_0380528c(value);break;
  case 19:return native_host_arm7_arm_03804c7c(value);
  case 20:native_host_arm7_arm_03804c00((value>>8)&255,value&255);break;
 }
 return 0;
}
