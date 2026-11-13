#include "context.h"
u32 native_ov001_02216460(void) {
 if (native_data_ov001_02242ba0.state1 == 0) {
  ov001_begin_state_transition_021f1354(1,0,33,1);
  ov001_select_mode_id_021f1438(native_fn_ov001_021f1414(1));
  native_fn_ov001_021d7f54(1);
  native_data_ov001_02242ba0.state1 = 5;
 } else if (native_data_ov001_02242ba0.state1 == 5) {
  native_fn_02041898(0);
  native_data_ov001_02242ba0.state1 = 10;
  native_data_ov001_02242ba0.counter0 = 0;
 } else if (native_data_ov001_02242ba0.state1 == 10) {
  native_data_ov001_02242ba0.counter0++;
  if (native_data_ov001_02242ba0.counter0 >= 30) native_data_ov001_02242ba0.state1 = 100;
 } else if (native_data_ov001_02242ba0.state1 == 20) {
  ov001_clear_state_flag4_021f14a4();
  native_data_ov001_02242ba0.state1 = 100;
 } else if (native_data_ov001_02242ba0.state1 == 100) {
  if (native_fn_ov001_021f14e4()) {
   native_data_ov001_02242ba0.field8 = 4;
   native_data_ov001_02242ba0.state1 = 0;
  }
  return 1;
 }
 return 0;
}
