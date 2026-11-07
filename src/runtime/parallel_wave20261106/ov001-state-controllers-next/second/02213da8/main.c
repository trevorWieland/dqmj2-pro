#include "context.h"
u32 native_ov001_02213da8(void) {
 if (native_data_ov001_02242aac.state2 == 0) {
  if (native_fn_ov001_021db8d0(native_data_ov001_02242aac.actor4)) {
   native_data_ov001_02242aac.state2 = 5;
  } else {
   return 1;
  }
 } else if (native_data_ov001_02242aac.state2 == 5) {
  native_fn_ov001_021f1294(16,2);
  native_fn_ov001_021f1354(11,0,native_data_ov001_02242abc[native_data_ov001_02242aac.selector0].value0,1);
  native_fn_ov001_021f1438(2);
  native_fn_ov001_021e9708(native_data_ov001_02242abc[native_data_ov001_02242aac.selector0].value0 == 0x31);
  native_fn_ov001_021e95d8(0);
  native_data_ov001_0222f1c8 = native_fn_ov001_021e9610(0);
  native_data_ov001_02242aac.state2 = 10;
 } else if (native_data_ov001_02242aac.state2 == 10) {
  if (native_fn_ov001_021ee410()) {
   native_fn_ov001_021f14a4();
   native_fn_ov001_021e9610(native_data_ov001_0222f1c8);
   native_data_ov001_02242aac.state2 = 100;
  }
 } else if (native_data_ov001_02242aac.state2 == 100) {
  native_fn_ov001_021f1324();
  native_data_ov001_02242aac.state2 = 0;
  return 1;
 }
 return 0;
}
