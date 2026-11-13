#include "context.h"
u32 native_ov001_021edd10(u32 payload) {
 if (native_data_ov001_02238d7c.state23 == 0) {
  native_fn_ov001_021d7e80(native_data_ov001_02238d7c.actor60);
  native_fn_ov001_021eaa3c(native_data_ov001_02238d7c.field36);
  ov001_select_mode_id_021f1438(native_fn_ov001_021f1414(native_data_ov001_02238d7c.actor60->field31e));
  native_data_ov001_02238d7c.state23 = 10;
  native_data_ov001_02238d7c.counter11 = 0;
 } else if (native_data_ov001_02238d7c.state23 == 10) {
  native_data_ov001_02238d7c.counter11++;
  if (native_data_ov001_02238d7c.counter11 >= 30) {
   native_fn_ov001_021eaa88(native_data_ov001_02238d7c.field36);
   native_data_ov001_02238d7c.state23 = 20;
  }
 } else if (native_data_ov001_02238d7c.state23 == 20) {
  if (!native_fn_ov001_021f14e4()) {
   ov001_begin_state_transition_021f1354(1,0,payload,1);
   native_data_ov001_02238d7c.state23 = 30;
   native_data_ov001_02238d7c.counter11 = 0;
  }
 } else if (native_data_ov001_02238d7c.state23 == 30) {
  native_data_ov001_02238d7c.counter11++;
  if (native_data_ov001_02238d7c.counter11 >= 30) {
   ov001_clear_state_flag4_021f14a4();
   native_data_ov001_02238d7c.state23 = 100;
  }
 } else if (native_data_ov001_02238d7c.state23 == 100) {
  if (!native_fn_ov001_021f14e4()) {
   native_data_ov001_02238d7c.field13 = 19;
   native_data_ov001_02238d7c.state23 = 0;
  }
 }
 return 0;
}
