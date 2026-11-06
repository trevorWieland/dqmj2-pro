typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef struct { u8 state; u8 reserved; u16 ticks; } RecoveryState;
typedef struct { u8 prefix[0x7c]; u32 flags; } RecoveryFlags;
typedef struct { u8 status; signed char heap; u16 reserved; int (*validator)(void *); u8 *buffer; } SaveIo;
extern RecoveryState native_recovery_state;
extern RecoveryFlags native_recovery_flags;
extern SaveIo native_save_io;
extern u8 native_save_prefix[];
extern int native_save_read(u32, void *, u32);
extern int save_load_backup_async(int);
extern int save_load_async_poll(void);
extern u32 save_write_status(void);
extern int save_write_start(int);
extern int save_write_poll(void);
extern void native_recovery_message_open(int, int, int, int, int, int);
extern void native_recovery_message_close(int);
int save_recovery_prefix_read(void) {
    if (native_save_read(0, native_save_prefix, 8)) {
        native_save_io.status = 0;
        return 1;
    }
    native_save_io.status = 2;
    return 0;
}
int save_recovery_update(u8 *phase, u32 *error) {
    int done = 0;
    if (!native_recovery_state.state) {
        native_recovery_state.ticks = 0;
        if (save_recovery_prefix_read()) native_recovery_state.state = 10;
        else native_recovery_state.state = 100;
    }
    if (native_recovery_state.state == 10) {
        if (save_load_backup_async(9)) {
            native_recovery_message_open(5, 6, 0x34, 0, 1, 0x52);
            native_recovery_state.state = 15;
        } else native_recovery_state.state = 105;
    }
    if (native_recovery_state.state == 15) {
        if (save_load_async_poll()) {
            u32 status = save_write_status();
            if (!status) native_recovery_state.state = 20;
            else if (status == 2) native_recovery_state.state = 105;
            else native_recovery_state.state = 110;
        }
    }
    if (native_recovery_state.state == 20) {
        if (save_write_start(9)) native_recovery_state.state = 25;
        else native_recovery_state.state = 107;
    }
    if (native_recovery_state.state == 25) {
        if (save_write_poll()) {
            u32 status = save_write_status();
            if (!status) native_recovery_state.state = 30;
            else if (status == 1) native_recovery_state.state = 107;
            else native_recovery_state.state = 110;
        }
    }
    if (native_recovery_state.state == 30) {
        *phase = 19;
        native_recovery_state.state = 150;
    }
    if (native_recovery_state.state == 100) {
        *error = 0x50000000;
        *phase = 3;
        native_recovery_state.state = 200;
    }
    if (native_recovery_state.state == 105) {
        *error = 0x50000000;
        *phase = 3;
        native_recovery_state.state = 150;
    }
    if (native_recovery_state.state == 107) {
        *error = 0x20000000;
        *phase = 3;
        native_recovery_state.state = 150;
    }
    native_recovery_state.ticks++;
    if (native_recovery_state.state == 110 && native_recovery_state.ticks > 90) {
        *phase = 16;
        native_recovery_state.state = 150;
    }
    if (native_recovery_state.state == 150 && native_recovery_state.ticks > 90) {
        native_recovery_message_close(0);
        native_recovery_state.state = 200;
    }
    if (native_recovery_state.state == 200) {
        native_recovery_state.state = 0;
        native_recovery_flags.flags &= ~2;
        done = 1;
    }
    return done;
}
