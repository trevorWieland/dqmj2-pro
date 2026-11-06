#include "context.h"

int native_main_020cc220(void) {
    int result = 0;
    switch(native_data_021d6714) {
    case 2:
        native_fn_020cd4e8(0x26,0x57);
        native_fn_020c48f8(3);
        native_data_021d6714 = 3;
        result = 1;
        break;
    case 3:
        native_fn_020cd4e8(0x27,0x57);
        native_fn_020c48f8(1);
        native_data_021d6714 = 0;
        result = 1;
        break;
    }
    return result;
}
