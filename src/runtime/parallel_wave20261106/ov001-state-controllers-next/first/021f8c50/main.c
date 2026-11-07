#include "context.h"
u32 native_ov001_021f8c50(u32 payload) {
 if (native_data_ov001_0223989c.state1e == 0) {
  native_fn_ov001_021f1324();
  native_data_ov001_0223989c.state1e = 10;
 } else if (native_data_ov001_0223989c.state1e == 10) {
  native_fn_ov001_021f1294(16, 2);
  native_fn_ov001_021d7e80(native_data_ov001_0223989c.actor84);
  native_data_ov001_0223989c.state1e = 20;
 } else if (native_data_ov001_0223989c.state1e == 20) {
  native_fn_ov001_021f1354(1, 0, payload, 1);
  native_fn_ov001_021f1438(native_fn_ov001_021f1414(native_data_ov001_0223989c.actor84->field31e));
  native_data_ov001_0223989c.state1e = 30;
  native_data_ov001_0223989c.counter1d = 0;
 }
 if (native_data_ov001_0223989c.state1e == 30) {
  native_data_ov001_0223989c.counter1d++;
  if (native_data_ov001_0223989c.counter1d > 45) native_data_ov001_0223989c.state1e = 100;
 }
 if (native_data_ov001_0223989c.state1e == 100) {
  native_data_ov001_0223989c.state1e = 0;
  native_fn_ov001_021f14a4();
  native_data_ov001_0223989c.field1b = 27;
 }
 return 0;
}
