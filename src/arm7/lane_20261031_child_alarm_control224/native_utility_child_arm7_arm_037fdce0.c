#include "native_alarm_types.h"
void native_utility_child_arm7_arm_037fdce0(void) {
    if (native_utility_child_arm7_alarm_initialized_03805b68 == 0) {
        native_utility_child_arm7_alarm_initialized_03805b68 = 1;
        native_utility_child_arm7_arm_037fd708(1);
        native_utility_child_arm7_alarm_queue_03805b6c.head = NULL;
        native_utility_child_arm7_alarm_queue_03805b6c.tail = NULL;
        native_utility_child_arm7_arm_037fbc50(16);
    }
}
