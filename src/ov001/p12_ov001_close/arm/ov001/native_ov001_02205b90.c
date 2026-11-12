/* ov001 row 0x02205b90: 244 bytes.
 *
 * What it does: 60 instructions; 4 call(s) to 0x0205f98c, 0x02048a44, 0x02205a70, +1 more; loops (back edge at +0x10); returns through pop {r4, r5, r6, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 4 calls (60 instructions, 4 calls, 8 branches, 4 back edges, 1 literal slot).
 *
 *   pool +0xf0 -> constant 0x0223d904 (image word 0x0223d904)
 *   branch +0x34 -> +0x58
 *   branch +0x64 -> +0x74
 *   branch +0x84 -> +0xe8
 *   branch +0x9c -> +0xe0
 *   branch +0xa8 -> +0xd4
 *   branch +0xd0 -> +0xe0
 *   test +0x30 cmp r0, #0
 *   test +0x60 cmp r0, #2
 *   test +0x78 cmp r0, #0
 *   test +0x98 cmp r0, r6
 *   test +0xa4 cmp r0, r1
 *   test +0xac cmp r0, #7
 *   0 block transfer(s), 8 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02205b90; the literal pool and
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

extern void native_fn_0205f98c(void);
extern void native_fn_02048a44(void);
extern void native_fn_02205a70(void);
extern void native_fn_022023a8(void);


asm u32 native_ov001_02205b90 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    mov r5, r0
    ldr r0, [r5, #0x1c]
    mov r1, #0
    bl native_fn_0205f98c
    ldr r3, [r5, #0x30]
    ldr r2, =0x0223d904
    mov r1, #12
    mla r1, r3, r1, r2
    ldr r2, [r5, #0x34]
    mov r4, r0
    ldr r0, [r1, r2, lsl #2]
    cmp r0, #0
    bne ov001_02205b90_L58
    mov r0, #0
    strh r0, [r5, #38]
    sub r1, r0, #1
    str r1, [r5, #0x2c]
    ldr r1, [r4, #0x7c]
    bic r1, r1, #2
    str r1, [r4, #0x7c]
    ldmia sp!, {r4, r5, r6, pc}
ov001_02205b90_L58:
    ldr r0, [r4, #0x7c]
    and r0, r0, #2
    cmp r0, #2
    bne ov001_02205b90_L74
    add r0, r4, #8
    mov r1, #1
    bl native_fn_02048a44
ov001_02205b90_L74:
    ldrsh r0, [r5, #38]
    cmp r0, #0
    subgt r0, r0, #2
    strgth r0, [r5, #38]
    bgt ov001_02205b90_Le8
    ldr r6, [r5, #0x2c]
    mov r0, r5
    bl native_fn_02205a70
    str r0, [r5, #0x2c]
    cmp r0, r6
    beq ov001_02205b90_Le0
    mvn r1, #0
    cmp r0, r1
    beq ov001_02205b90_Ld4
    cmp r0, #7
    addlt r0, r0, #99
    addge r0, r0, #186
    and r1, r0, #255
    mov r0, r4
    bl native_fn_022023a8
    ldr r0, [r4, #0x7c]
    orr r0, r0, #2
    str r0, [r4, #0x7c]
    b ov001_02205b90_Le0
ov001_02205b90_Ld4:
    ldr r0, [r4, #0x7c]
    bic r0, r0, #2
    str r0, [r4, #0x7c]
ov001_02205b90_Le0:
    mov r0, #120
    strh r0, [r5, #38]
ov001_02205b90_Le8:
    mov r0, #0
    ldmia sp!, {r4, r5, r6, pc}
}
