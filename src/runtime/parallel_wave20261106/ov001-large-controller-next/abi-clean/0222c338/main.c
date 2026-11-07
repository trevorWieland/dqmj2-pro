#include "context.h"
u32 native_ov001_0222c338(void) {
    native_fn_0207afec(0xd7);
    if (native_data_022497e8.state8 == 0) {
        native_fn_ov001_021d7f54(native_data_022497e8.selector0);
        native_fn_ov001_021f1354(1, 0, 0x31, 1);
        native_fn_ov001_021f1438(native_fn_ov001_021f1414(native_data_022497e8.selector0));
        native_data_022497e8.counter7 = 0;
        native_data_022497e8.state8 = 5;
    }
    if (native_data_022497e8.state8 == 5) {
        native_data_022497e8.counter7++;
        if (native_data_022497e8.counter7 > 30) native_data_022497e8.state8 = 10;
    }
    if (native_data_022497e8.state8 == 10) {
        Object440 *object;
        s32 i;
        i = 0;
        do {
            object = native_fn_ov001_021db438(native_data_022497e8.selector0, i);
            if (native_fn_ov001_021db8d0(object))
                native_fn_ov001_021dbf98(object, 8, 1, -1, 0);
            i++;
        } while (i < 3);
        native_data_022497e8.counter7 = 0;
        native_data_022497e8.state8 = 20;
    } else if (native_data_022497e8.state8 == 20) {
        native_data_022497e8.counter7++;
        if (native_data_022497e8.counter7 > 30) native_data_022497e8.state8 = 30;
    } else if (native_data_022497e8.state8 == 30) {
        Object440 *object;
        s32 i;
        native_fn_ov001_021f14a4();
        i = 0;
        do {
            object = native_fn_ov001_021db438(native_data_022497e8.selector0, i);
            if (native_fn_ov001_021db8d0(object))
                native_fn_ov001_021ee91c(object, object->field234);
            i++;
        } while (i < 3);
        native_data_022497e8.counter7 = 0;
        native_data_022497e8.state8 = 40;
    } else if (native_data_022497e8.state8 == 40) {
        native_data_022497e8.counter7++;
        if (native_data_022497e8.counter7 > 45) native_data_022497e8.state8 = 100;
    }
    if (native_data_022497e8.state8 == 100) {
        native_data_022497e8.state8 = 0;
        native_data_022497e8.field1 = 7;
    }
    return 0;
}
