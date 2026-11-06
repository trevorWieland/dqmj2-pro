#include "context.h"
static inline u32 disable_master(void){u32 previous=*(volatile u16*)0x04000208;*(volatile u16*)0x04000208=0;return previous;}
static inline u32 enable_master(void){u32 previous=*(volatile u16*)0x04000208;*(volatile u16*)0x04000208=1;return previous;}
static inline u32 restore_master(u32 value){u32 previous=*(volatile u16*)0x04000208;*(volatile u16*)0x04000208=(u16)value;return previous;}
void native_host_arm7_wram_03804fbc(u32 triggers,u32 keys,u32 flags)
{
 u32 previousMaster;
 u32 previousInterrupts,previousMask;
 u8 control;
 u16 previousSerial;
 s32 restoreSerial=0;
 u32 top,bottom;
 previousMaster=disable_master();
 previousInterrupts=native_host_arm7_arm_037fdd00();
 previousMask=native_host_arm7_arm_037fb928(0x01ffffff);
 control=native_host_arm7_arm_03804c7c(0);
 native_host_arm7_arm_0380528c(2);
 native_host_arm7_arm_03804f54(2);
 native_host_arm7_arm_03804f54(2);
 native_host_arm7_arm_037fe708();
 native_host_arm7_arm_03804d14(1);
 if(triggers&1){*(volatile u16*)0x04000132=(u16)(0x4000|keys);native_host_arm7_arm_037fb8f0(0x1000);}
 if(triggers&4)native_host_arm7_arm_037fb8f0(0x400000);
 if(triggers&2){
  previousSerial=*(volatile u16*)0x04000134;restoreSerial=1;
  native_host_arm7_arm_037fe5a8(0x8000);
  native_host_arm7_arm_037fe588(0x40,0);
  native_host_arm7_arm_037fe588(0x100,0x100);
  native_host_arm7_arm_037fb8f0(0x80);
 }
 if(triggers&8)native_host_arm7_arm_037fb8f0(0x100000);
 if(triggers&16)native_host_arm7_arm_037fb8f0(0x2000);
 native_host_arm7_arm_037fdd14(previousInterrupts);
 enable_master();
 native_host_arm7_arm_03805160();
 native_host_arm7_arm_03804c00(0,control);
 top=flags&0x40?6:7;bottom=flags&0x80?4:5;
 native_host_arm7_arm_03804d40(top,0);
 native_host_arm7_arm_03804d40(bottom,0);
 if(restoreSerial)*(volatile u16*)0x04000134=previousSerial;
 native_host_arm7_arm_03804cf0(1);
 native_host_arm7_arm_037fe760();
 native_host_arm7_work_03809eb0.status=0;
 native_host_arm7_wram_03804bc4(0x63,0);
 native_host_arm7_arm_037fdd00();
 native_host_arm7_arm_037fb8a4(previousMask);
 native_host_arm7_arm_037fdd14(previousInterrupts);
 restore_master(previousMaster);
}
