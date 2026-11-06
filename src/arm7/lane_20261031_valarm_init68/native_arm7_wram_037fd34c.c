typedef unsigned short u16;
typedef unsigned int u32;
typedef struct { u16 initialized; u16 pad; u32 head; u32 tail; } AlarmState;
extern AlarmState native_host_arm7_valarm_state_038078a8;
extern u32 native_host_arm7_arm_037fd10c(u32 timer);
extern u32 native_host_arm7_arm_037fb928(u32 mask);
u32 native_arm7_wram_037fd34c(void) {
    u32 result = native_host_arm7_valarm_state_038078a8.initialized;
    if (result == 0) {
        native_host_arm7_valarm_state_038078a8.initialized = 1;
        native_host_arm7_arm_037fd10c(1);
        native_host_arm7_valarm_state_038078a8.head = 0;
        native_host_arm7_valarm_state_038078a8.tail = 0;
        result = native_host_arm7_arm_037fb928(16);
    }
    return result;
}
