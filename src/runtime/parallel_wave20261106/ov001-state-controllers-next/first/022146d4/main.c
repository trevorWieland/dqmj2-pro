#include "context.h"
u32 native_ov001_022146d4(u32 payload) {
 if (native_data_ov001_02242b50.state9 == 0) {
  native_data_ov001_02242b50.counter8 = 0;
  native_data_ov001_02242b50.state9 = 2;
 } else if (native_data_ov001_02242b50.state9 == 2) {
  native_data_ov001_02242b50.counter8++;
  if (native_data_ov001_02242b50.counter8 > 30) native_data_ov001_02242b50.state9 = 5;
 } else if (native_data_ov001_02242b50.state9 == 5) {
  native_fn_ov001_021f1324();
  native_data_ov001_02242b50.state9 = 10;
 } else if (native_data_ov001_02242b50.state9 == 10) {
  native_fn_ov001_021f1294(16, 2);
  native_data_ov001_02242b50.state9 = 20;
 } else if (native_data_ov001_02242b50.state9 == 20) {
  native_fn_ov001_021f1354(1, 0, payload, 1);
  native_fn_ov001_021f1438(native_fn_ov001_021f1414(native_data_ov001_02242b50.actor10->field31e));
  native_data_ov001_02242b50.state9 = 30;
  native_data_ov001_02242b50.counter8 = 0;
 }
 if (native_data_ov001_02242b50.state9 == 30) {
  native_data_ov001_02242b50.counter8++;
  if (native_data_ov001_02242b50.counter8 > 45) native_data_ov001_02242b50.state9 = 100;
 }
 if (native_data_ov001_02242b50.state9 == 100) {
  native_data_ov001_02242b50.state9 = 0;
  native_fn_ov001_021f14a4();
  native_data_ov001_02242b50.field2 = 5;
 }
 return 0;
}
