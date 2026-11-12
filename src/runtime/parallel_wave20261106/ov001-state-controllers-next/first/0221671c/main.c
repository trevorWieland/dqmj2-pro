#include "context.h"
u32 native_ov001_0221671c(void) {
 if (native_data_ov001_02242be8.state2 == 0) {
  native_fn_ov001_021d7e80(native_data_ov001_02242be8.actor8);
  native_data_ov001_02242be8.actor8->field325 = 1;
  native_fn_ov001_022025a4(native_data_ov001_02242be8.actor8->field31e,native_data_ov001_02242be8.actor8->field31f);
  ov001_begin_state_transition_021f1354(7,0,native_data_ov001_02242be8.field4,1);
  ov001_select_mode_id_021f1438(native_fn_ov001_021f1414(native_data_ov001_02242be8.actor8->field31e));
  native_data_ov001_02242be8.state2 = 10;
  native_data_ov001_02242be8.counter3 = 0;
 } else if (native_data_ov001_02242be8.state2 == 10) {
  native_data_ov001_02242be8.counter3++;
  if (native_data_ov001_02242be8.counter3 >= 40) native_data_ov001_02242be8.state2 = 100;
 } else if (native_data_ov001_02242be8.state2 == 100) {
  ov001_clear_state_flag4_021f14a4();
  native_data_ov001_02242be8.state2 = 0;
  native_data_ov001_02242be8.field1 = 3;
 }
 return 0;
}
