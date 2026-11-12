/* ov000 row 0x021fe3ec: 100 bytes.
 *
 * What it does: 24 instructions and 3 call(s), then a 11-entry dispatch through an inline branch table at 0x021fe408 (dispatch word at 0x021fe400)
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
extern void native_fn_021fe78c(void);
extern void native_fn_021fe7f0(void);


asm u32 native_ov000_021fe3ec (register u32 a0)
{
    stmdb sp!, {r3, lr}
    bl ov000_display_context_02215698
    ldrb r1, [r0, #0x494]
    ldr r0, [pc, #0x4c]
    cmp r1, #10
    addls pc, pc, r1, lsl #2
    b L_021fe434
    dcd 0xea000009
    dcd 0xea000008
    dcd 0xea000007
    dcd 0xea000008
    dcd 0xea000007
    dcd 0xea000004
    dcd 0xea000003
    dcd 0xea000002
    dcd 0xea000001
    dcd 0xea000002
    dcd 0xea000001
L_021fe434:
    mov r0, #0
    ldmia sp!, {r3, pc}
    bl native_fn_021fe78c
    bl native_fn_021fe7f0
    mov r0, #0
    ldmia sp!, {r3, pc}
    dcd 0x022372c4
}
