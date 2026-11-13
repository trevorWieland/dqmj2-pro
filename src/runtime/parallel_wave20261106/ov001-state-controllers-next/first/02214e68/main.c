#include "context.h"
u32 native_ov001_02214e68(void) {
 if ((s8)native_data_ov001_02242b94.state0 == 0) {
  if (native_fn_ov001_021f90b4()) native_data_ov001_02242b94.state0 = 10;
 } else if ((s8)native_data_ov001_02242b94.state0 == 10) {
  native_fn_020414b0(1);
  native_fn_02041510(1,2,60);
  native_data_ov001_02242b94.state0 = 20;
 } else if ((s8)native_data_ov001_02242b94.state0 == 20) {
  if (native_fn_02041800() != 1) {
   native_fn_020414b0(63);
   native_fn_ov001_021f1294(16,2);
   ov001_begin_state_transition_021f1354(1,0,34,1);
   native_fn_02048034(native_data_ov001_02242b94.actor8->child1e8+0xb2,0);
   native_data_ov001_02242b94.state0 = 30;
   native_data_ov001_02242b94.counter2 = 0;
  }
 } else if ((s8)native_data_ov001_02242b94.state0 == 30) {
  native_data_ov001_02242b94.counter2++;
  if (native_data_ov001_02242b94.counter2 >= 60) {
   ov001_clear_state_flag4_021f14a4();
   native_data_ov001_02242b94.state0 = 100;
  }
 } else if ((s8)native_data_ov001_02242b94.state0 == 100) {
  if (native_fn_ov001_021f14e4()) {
   native_fn_ov001_021f1324();
   native_data_ov001_02242b94.state0 = 0;
   native_data_ov001_02242b94.field3 = 4;
   native_data_ov001_02242b94.field1 = 1;
   return 1;
  }
 }
 return 0;
}
