/* ov000 row 0x021e7534: 128 bytes.
 *
 * What it does: 29 instructions and 4 call(s), then a 5-entry dispatch through an inline branch table at 0x021e7550 (dispatch word at 0x021e7548)
 *
 * Carrier: mwccarm asm with dcd data runs.
 * The measured extent is code plus data inside the function. The data
 * runs are emitted as data, not decoded as instructions; every
 * instruction, branch target, pool word and table entry is read from
 * the image.
 *
 * Unknowns: the field roles, the meaning of the table entries and every callee contract are not established by byte identity; the dispatch range and the table bounds are measured.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_0205c668(void);


asm u32 native_ov000_021e7534 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr r0, [pc, #0x68]
    mov r1, #0
    ldrb r0, [r0]
    cmp r0, #4
    addls pc, pc, r0, lsl #2
    b L_021e75a0
    dcd 0xea000012
    dcd 0xea000002
    dcd 0xea000005
    dcd 0xea000008
    dcd 0xea00000b
    mov r0, #248
    bl native_fn_0205c668
    mov r1, r0
    b L_021e75a0
    ldr r0, [pc, #0x30]
    bl native_fn_0205c668
    mov r1, r0
    b L_021e75a0
    ldr r0, [pc, #0x24]
    bl native_fn_0205c668
    mov r1, r0
    b L_021e75a0
    mov r0, #260
    bl native_fn_0205c668
    mov r1, r0
L_021e75a0:
    mov r0, r1
    ldmia sp!, {r3, pc}
    dcd 0x022351d4
    dcd 0x00000102
    dcd 0x00000103
}
