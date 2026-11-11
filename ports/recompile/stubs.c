/* Minimal platform stub layer for the standalone link test.
 *
 * Every symbol here is an import of the two reconstructed boot functions:
 *   - src/main/p3g_main_02000c34/native_main_02000c34.c   (matched main, 80 B)
 *   - src/main/p3g_main_02000c34/native_main_020c225c.c   (matched boot-floor function, 104 B)
 *
 * The bodies are deliberately empty or constant: this is a link target, not an emulator. A real
 * port replaces these with the services listed in docs/platform/contract.md section 1. Two return
 * values are chosen so the boot loop takes its early path (native_fn_020271ec returns 0 so main
 * keeps looping; native_fn_02084718 returns 1 so the one-shot block is skipped).
 */

typedef unsigned char u8;
typedef unsigned int u32;

/* Data the reconstructed functions reference. Sized to the offsets they touch (0x10 and 0x18). */
u8 native_data_020ec9b8[0x40];
u8 native_data_021d4c3c[0x40];

/* main() imports. */
void native_fn_02026b28(void) {}
void native_fn_02026ec0(void) {}
void native_fn_020ba490(void) {}
void native_fn_0202718c(void) {}
u32  native_fn_020271ec(void) { return 0; }
void native_fn_02026f70(void) {}
void native_fn_0205f4f4(void) {}
void native_fn_020270d4(void) {}
void native_fn_020c225c(void) {}
void native_fn_020270d8(void) {}

/* 0x020C225C imports. */
void native_fn_02089804(void) {}
void native_fn_02006b7c(u32 value) { (void)value; }
u32  native_fn_02084718(void) { return 1; }
void native_fn_02084180(u32 value) { (void)value; }
void native_fn_020841b8(void) {}
void native_fn_020c2528(void) {}
