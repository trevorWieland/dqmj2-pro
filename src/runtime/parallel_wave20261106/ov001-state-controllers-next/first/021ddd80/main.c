#include "context.h"
u32 native_ov001_021ddd80(void) {
 s32 mode = native_fn_02044554();
 if (native_data_ov001_022388ec.state2 == 0) {
  native_fn_ov001_021d7e30(1);
  native_fn_ov001_021f1294(16,2);
  if (mode == 1) mode = 6; else mode = 7;
  native_fn_ov001_021d94cc(0,1);
  ov001_begin_state_transition_021f1354(1,0,mode,1);
  native_data_ov001_022388ec.state2 = 10;
  native_data_ov001_022388ec.counterD = 0;
 } else if (native_data_ov001_022388ec.state2 == 10) {
  native_data_ov001_022388ec.counterD++;
  if (native_data_ov001_022388ec.counterD >= 30) {
   ov001_clear_state_flag4_021f14a4();
   native_data_ov001_022388ec.state2 = 100;
  }
 } else if (native_data_ov001_022388ec.state2 == 100) {
  if (native_fn_ov001_021f14e4()) {
   if (mode == 1) {
    native_data_ov001_022388ec.field8 = 1;
    native_data_ov001_022388ec.field7 = 1;
   } else {
    native_fn_ov001_021e7fa8();
    native_data_ov001_022388ec.field8 = 3;
    native_data_ov001_022388ec.field1b = 1;
   }
   native_fn_ov001_021f1324();
   native_data_ov001_022388ec.state2 = 0;
   native_fn_ov001_021d7e30(0);
   return 1;
  }
 }
 return 0;
}
