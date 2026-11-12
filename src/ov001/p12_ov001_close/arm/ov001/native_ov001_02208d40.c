/* ov001 row 0x02208d40: 304 bytes.
 *
 * What it does: 75 instructions; 7 call(s) to 0x02207938, 0x020852d0, 0x02208dfc, +4 more; loops (back edge at +0x08); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 7 calls (75 instructions, 7 calls, 1 branch, 6 back edges, 1 literal slot).
 *
 *   pool +0x12c -> native_data_0222e0e0 (image word 0x0222e0e0)
 *   branch +0x4c -> +0xe0
 *   branch +0x94 -> +0xbc
 *   back edge +0xc8 -> +0x88
 *   back edge +0xdc -> +0x68
 *   test +0x48 cmp r0, #0
 *   test +0x70 cmp r0, #0
 *   test +0x90 cmp r3, #2
 *   test +0xc0 cmp r8, #6
 *   test +0xd8 cmp r0, #2
 *   test +0xe0 cmp r10, #0
 *   0 block transfer(s), 13 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02208d40; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity fixes the instruction stream, not the field, block and callee semantics behind the addresses and strides it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_02207938(void);
extern u8 native_data_0222e0e0[];
extern void native_fn_020852d0(void);
extern void native_fn_0204a3ec(void);
extern void native_fn_0204a574(void);


asm u32 native_ov001_02208d40 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #20
    bl native_fn_02207938
    mov r4, r0
    ldr r0, =native_data_0222e0e0
    ldr r1, [r4, #0x8]
    mov r10, #0
    ldr r1, [r1]
    ldrh r3, [r0]
    ldrh r2, [r0, #2]
    ldr r0, [r1, #0x4]
    ldr r7, [r4, #0x10]
    mov r1, r10
    strh r3, [sp, #16]
    strh r2, [sp, #18]
    ldr r9, [r4, #0x540]
    bl native_fn_020852d0
    ldr r0, [r4, #0x544]
    cmp r0, #0
    beq ov001_02208d40_Le0
    mov r0, r10
    str r0, [sp, #0xc]
    mov r6, r10
    mov r5, #26
    add r4, sp, #16
    mov r11, #1
ov001_02208d40_L68:
    ldr r0, [sp, #0xc]
    mov r8, #0
    cmp r0, #0
    moveq r0, #8
    movne r0, #128
    strh r0, [sp, #16]
    mov r0, r8
    strh r0, [sp, #18]
ov001_02208d40_L88:
    add r0, r7, r9
    ldrb r3, [r0, #0x35e]
    cmp r3, #2
    blo ov001_02208d40_Lbc
    mov r0, r5
    str r6, [sp]
    mov r1, r4
    mov r2, r11
    bl native_fn_0204a3ec
    ldrsh r0, [sp, #18]
    mov r10, #1
    add r0, r0, #16
    strh r0, [sp, #18]
ov001_02208d40_Lbc:
    add r8, r8, #1
    cmp r8, #6
    add r9, r9, #1
    blt ov001_02208d40_L88
    ldr r0, [sp, #0xc]
    add r0, r0, #1
    str r0, [sp, #0xc]
    cmp r0, #2
    blt ov001_02208d40_L68
ov001_02208d40_Le0:
    cmp r10, #0
    addne sp, sp, #20
    ldmneia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
    mov r0, #8
    mov r4, #0
    strh r0, [sp, #16]
    strh r4, [sp, #18]
    mov r0, #63
    str r0, [sp]
    mov r0, #1
    str r0, [sp, #0x4]
    add r1, sp, #16
    mov r0, #26
    mov r2, #5
    mov r3, #3
    str r4, [sp, #0x8]
    bl native_fn_0204a574
    add sp, sp, #20
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
