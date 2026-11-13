#include "context.h"
u32 native_ov001_021df808(void) {
 if (native_data_ov001_022388ec.state2e == 0) {
  native_fn_ov001_021d7e80(native_data_ov001_022388ec.actor48);
  native_fn_ov001_021f1294(16, 2);
  ov001_begin_state_transition_021f1354(1, 0, 0x38, 1);
  ov001_select_mode_id_021f1438(native_data_ov001_022388ec.actor48->field31e);
  native_data_ov001_022388ec.counter2d = 0;
  native_data_ov001_022388ec.state2e = 10;
 } else if (native_data_ov001_022388ec.state2e == 10) {
  native_data_ov001_022388ec.counter2d++;
  if (native_data_ov001_022388ec.counter2d >= 30) {
   native_data_ov001_022388ec.state2e = 100;
   ov001_clear_state_flag4_021f14a4();
  }
 } else if (native_data_ov001_022388ec.state2e == 100) {
  native_fn_ov001_021f1324();
  native_data_ov001_022388ec.field8 = 15;
  native_data_ov001_022388ec.state2e = 0;
  return 1;
 }
 return 0;
}
