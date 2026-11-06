#include "context.h"
void native_host_arm7_wram_0380516c(void)
{
 s32 next=native_host_arm7_led_state_038075dc;
 BlinkRecord *record;
 if(native_host_arm7_blink_state_03809edc.pattern==0){
  if(native_host_arm7_arm_03803b7c(3,0x64,1,1))native_host_arm7_arm_0380528c(1);
  return;
 }else if(native_host_arm7_blink_state_03809edc.pattern<4){
  if(native_host_arm7_blink_state_03809edc.pattern!=native_host_arm7_led_state_038075dc)native_host_arm7_arm_03803b7c(3,0x64,1,native_host_arm7_blink_state_03809edc.pattern);
  return;
 }
 record=&native_host_arm7_blink_records_038075e0[native_host_arm7_blink_state_03809edc.pattern-4];
 if(record->bits&(0x8000000000000000ULL>>(native_host_arm7_blink_state_03809edc.counter/record->resolution)))next=1;
 else next=2;
 native_host_arm7_blink_state_03809edc.counter++;
 if(native_host_arm7_blink_state_03809edc.counter>=record->length*record->resolution)native_host_arm7_blink_state_03809edc.counter=0;
 if(next!=native_host_arm7_led_state_038075dc)native_host_arm7_arm_03803b7c(3,0x64,1,next);
}
