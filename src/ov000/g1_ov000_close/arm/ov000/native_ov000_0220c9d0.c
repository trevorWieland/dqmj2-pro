/* ov000 row 0x0220c9d0: 264 bytes.
 *
 * What it does: 66 instructions and 10 call(s), then a 5-entry dispatch through an inline branch table at 0x0220ca68 (dispatch word at 0x0220ca60)
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

extern void native_fn_0205cba4(void);
extern void native_fn_021e7b9c(void);
extern void native_fn_021e07b8(void);
extern void native_fn_020420c4(void);
extern void native_fn_020c56b4(void);
extern void native_fn_0220c6c8(void);
extern void native_fn_0220c768(void);
extern void native_fn_0220c884(void);
extern void native_fn_0220c82c(void);


asm u32 native_ov000_0220c9d0 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r5, r0
    ldrb r0, [r5, #0x279]
    mov r4, #0
    cmp r0, #0
    bne L_0220ca40
    ldrb r0, [r5, #0x1e2]
    cmp r0, #0
    beq L_0220ca18
    ldrb r0, [r5, #0x160]
    cmp r0, #10
    bls L_0220ca18
    mov r1, r5
    mov r0, #6
    mov r2, #1
    bl native_fn_0205cba4
    mov r0, #146
    bl native_fn_021e7b9c
L_0220ca18:
    mov r0, #0
    bl native_fn_021e07b8
    mov r1, r0
    mov r0, r5
    bl native_fn_020420c4
    add r0, r5, #512
    mov r1, #0
    strh r1, [r0, #122]
    mov r0, #10
    strb r0, [r5, #0x279]
L_0220ca40:
    ldrb r0, [r5, #0x279]
    cmp r0, #10
    bne L_0220cac4
    add r0, r5, #512
    ldrsh r0, [r0, #118]
    bl native_fn_020c56b4
    ldrb r0, [r0, #0x6]
    cmp r0, #4
    addls pc, pc, r0, lsl #2
    b L_0220caa0
    dcd 0xea00000c
    dcd 0xea000002
    dcd 0xea000004
    dcd 0xea000003
    dcd 0xea000005
    mov r0, r5
    bl native_fn_0220c6c8
    b L_0220caa8
    mov r0, r5
    bl native_fn_0220c768
    b L_0220caa8
    mov r0, r5
    bl native_fn_0220c884
    b L_0220caa8
L_0220caa0:
    mov r0, r5
    bl native_fn_0220c82c
L_0220caa8:
    cmp r0, #0
    beq L_0220cac4
    add r0, r5, #512
    mov r1, #31
    strh r1, [r0, #122]
    mov r0, #20
    strb r0, [r5, #0x279]
L_0220cac4:
    ldrb r0, [r5, #0x279]
    cmp r0, #20
    moveq r4, #1
    mov r0, r4
    ldmia sp!, {r3, r4, r5, pc}
}
