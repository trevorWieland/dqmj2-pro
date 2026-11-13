/* ov000 row 0x021d8958: 176 bytes.
 *
 * What it does: 39 instructions and 7 call(s), then a 4-entry dispatch through an inline branch table at 0x021d896c (dispatch word at 0x021d8964)
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

extern void native_fn_021d8a18(void);
extern void ov000_saved_world_position_get_021e07b8(void);
extern void native_fn_021d8548(void);
extern void native_fn_0202818c(void);


asm u32 native_ov000_021d8958 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    bl native_fn_021d8a18
    cmp r0, #3
    addls pc, pc, r0, lsl #2
    ldmia sp!, {r3, pc}
    dcd 0xea000002
    dcd 0xea000006
    dcd 0xea00000a
    dcd 0xea000018
    mov r0, #0
    bl ov000_saved_world_position_get_021e07b8
    mov r1, #1
    bl native_fn_021d8548
    ldmia sp!, {r3, pc}
    ldr r0, [pc, #0x5c]
    mov r1, #0
    ldr r0, [r0, #0x8]
    bl native_fn_021d8548
    ldmia sp!, {r3, pc}
    ldr lr, [pc, #0x4c]
    ldr r12, [pc, #0x4c]
    ldmia lr, {r0, r1, r2}
    ldr r3, [pc, #0x3c]
    stmia r12, {r0, r1, r2}
    ldr r12, [r3, #0x8]
    ldr r3, [pc, #0x3c]
    ldmia r12, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    mov r0, r12
    mov r1, lr
    bl native_fn_0202818c
    ldr r1, [pc, #0x28]
    str r0, [r1, #0x4c]
    ldmia sp!, {r3, pc}
    mov r0, #0
    bl ov000_saved_world_position_get_021e07b8
    mov r1, #0
    bl native_fn_021d8548
    ldmia sp!, {r3, pc}
    dcd 0x02230318
    dcd 0x02230398
    dcd 0x02230358
    dcd 0x02230364
    dcd 0x0223033c
}
