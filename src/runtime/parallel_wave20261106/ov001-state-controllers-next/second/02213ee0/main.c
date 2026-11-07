#include "context.h"
u32 native_ov001_02213ee0(void) {
 if (native_data_ov001_02242aac.state2 == 0) {
  if (!native_fn_ov001_021db8d0(native_data_ov001_02242aac.actor4)) return 1;
  if (native_data_ov001_02242aac.actor4->field1e4 == 0) {
   native_data_ov001_02242aac.state2 = 5;
   native_fn_ov001_021f1294(16,2);
   native_fn_ov001_021f1354(11,0,native_data_ov001_02242abc[native_data_ov001_02242aac.selector0].value0,1);
   native_fn_ov001_021f1438(2);
  }
 } else if (native_data_ov001_02242aac.state2 == 5) {
  native_fn_ov001_021d7e80(native_data_ov001_02242aac.actor4);
  native_fn_ov001_021d9494(native_data_ov001_02242aac.actor4,4,1);
  native_data_ov001_02242aac.state2 = 10;
  native_data_ov001_02242aac.counter3 = 0;
 } else if (native_data_ov001_02242aac.state2 == 10) {
  native_data_ov001_02242aac.counter3++;
  if (native_data_ov001_02242aac.counter3 > 30) native_data_ov001_02242aac.state2 = 20;
 } else if (native_data_ov001_02242aac.state2 == 20) {
  native_fn_ov001_021dbf98(native_data_ov001_02242aac.actor4,native_data_ov001_02242abd[native_data_ov001_02242aac.selector0].value0,1,0,1);
  native_fn_ov001_022142c0();
  native_fn_ov001_021e2078();
  native_data_ov001_02242aac.state2 = 30;
  native_fn_ov001_021f14a4();
  native_data_ov001_02242aac.counter3 = 0;
 } else if (native_data_ov001_02242aac.state2 == 30) {
  native_data_ov001_02242aac.counter3++;
  if (native_data_ov001_02242aac.counter3 > 15) {
   native_fn_ov001_021f1324();
   native_data_ov001_02242aac.state2 = 0;
   return 1;
  }
 }
 return 0;
}
