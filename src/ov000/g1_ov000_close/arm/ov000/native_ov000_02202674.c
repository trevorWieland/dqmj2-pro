/* ov000 row 0x02202674: 148 bytes.
 *
 * What it does: 36 instructions and 2 call(s), then a 4-entry dispatch through an inline branch table at 0x02202698 (dispatch word at 0x02202690)
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

extern void ov000_display_context_02215698(void);
extern void native_fn_0204b53c(void);


asm u32 native_ov000_02202674 (register u32 a0)
{
    stmdb sp!, {r3, r4, lr}
    sub sp, sp, #4
    mov r4, r0
    bl ov000_display_context_02215698
    ldr r1, [pc, #0x78]
    ldr r1, [r1]
    cmp r1, #3
    addls pc, pc, r1, lsl #2
    b L_022026d0
    dcd 0xea000002
    dcd 0xea000001
    dcd 0xea000005
    dcd 0xea000004
    mov r2, #16
    mov r1, #40
    strh r2, [sp]
    strh r1, [sp, #2]
    b L_022026d8
    mov r2, #16
    mov r1, #48
    strh r2, [sp]
    strh r1, [sp, #2]
    b L_022026d8
L_022026d0:
    add sp, sp, #4
    ldmia sp!, {r3, r4, pc}
L_022026d8:
    ldrsh r12, [sp, #2]
    ldr r3, [r4]
    ldr r2, [r4, #0x4]
    add r1, sp, #0
    sub r2, r3, r2
    add r2, r12, r2, lsl #4
    add r0, r0, #16
    strh r2, [sp, #2]
    bl native_fn_0204b53c
    add sp, sp, #4
    ldmia sp!, {r3, r4, pc}
    dcd 0x02237d94
}
