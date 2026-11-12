/* Record a selection and its mode, then notify the listener.
 *
 * The word goes to 0x0222f548, the byte to 0x02238190+3, and the mode to +2:
 * a mode of -1 means "derive from the selection" (above five becomes 1, else 0),
 * any other mode is stored as given. A non-zero last argument runs the notifier.
 * Unknowns: what the selection is and what the notifier consumes.
 */
typedef unsigned char u8;
typedef unsigned int u32;
typedef signed int s32;

#define M2C_FIELD(value, type, offset) (*(type)((u8 *)(value) + (offset)))

extern u8 native_data_ov000_0222f548[];
extern u8 native_data_ov000_02238190[];
extern void native_fn_ov000_02202938(void);

void native_ov000_0220552c(u32 selection, u8 index, s32 mode, s32 notify)
{
    M2C_FIELD(native_data_ov000_0222f548, u32 *, 0) = selection;
    M2C_FIELD(native_data_ov000_02238190, u8 *, 3) = index;
    if (mode == -1) {
        M2C_FIELD(native_data_ov000_02238190, u8 *, 2) = (index > 5) ? 1 : 0;
    } else {
        M2C_FIELD(native_data_ov000_02238190, u8 *, 2) = mode;
    }
    if (notify != 0)
        native_fn_ov000_02202938();
}
