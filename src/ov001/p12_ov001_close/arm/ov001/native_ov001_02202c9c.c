/* ov001 row 0x02202c9c: 240 bytes.
 *
 * What it does: 58 instructions; 10 call(s) to 0x0206d230, 0x02008e0c, 0x0202a498, +7 more; loops (back edge at +0x04); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 10 calls (58 instructions, 10 calls, 2 branches, 10 back edges, 2 literal slots).
 *
 *   pool +0xe8 -> constant 0x0223a030 (image word 0x0223a030)
 *   pool +0xec -> constant 0x02239c10 (image word 0x02239c10)
 *   branch +0x28 -> +0x40
 *   branch +0x7c -> +0xc4
 *   back edge +0xc0 -> +0x88
 *   back edge +0xe0 -> +0x5c
 *   test +0x24 cmp r1, #0
 *   test +0x48 cmp r0, #22
 *   test +0x5c cmp r8, #0
 *   test +0x78 cmp r9, #0
 *   test +0xb8 cmp r9, r0, asr #24
 *   test +0xdc cmp r8, #2
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02202c9c; the literal pool and
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

extern void native_fn_0206d230(void);
extern void native_fn_02008e0c(void);
extern void native_fn_0202a498(void);
extern void native_fn_021db530(void);
extern void native_fn_021fd074(void);
extern void native_fn_021db438(void);
extern void native_fn_0206d114(void);
extern void native_fn_021fcd14(void);


asm u32 native_ov001_02202c9c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    bl native_fn_0206d230
    ldr r2, =0x0223a030
    mov r1, r0
    ldr r0, [r2, #0x204]
    mov r2, #360
    bl native_fn_02008e0c
    ldr r0, =0x0223a030
    ldr r1, [r0, #0x204]
    cmp r1, #0
    beq ov001_02202c9c_L40
    mov r0, #2
    bl native_fn_0202a498
    ldr r0, =0x0223a030
    mov r1, #0
    str r1, [r0, #0x204]
ov001_02202c9c_L40:
    ldr r0, =0x02239c10
    ldrb r0, [r0, #0xa]
    cmp r0, #22
    ldmeqia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    mov r8, #0
    mov r4, #1
    mov r11, r8
ov001_02202c9c_L5c:
    cmp r8, #0
    moveq r10, r11
    movne r10, #1
    mov r0, r10
    bl native_fn_021db530
    mov r9, r0
    mov r7, #0
    cmp r9, #0
    ble ov001_02202c9c_Lc4
    mov r0, r10, lsl #24
    mov r6, r0, asr #24
ov001_02202c9c_L88:
    mov r0, r6
    mov r1, r7
    bl native_fn_021fd074
    mov r5, r0
    mov r0, r10
    mov r1, r7
    bl native_fn_021db438
    ldrsb r0, [r5, #12]
    mov r1, r4
    bl native_fn_0206d114
    add r0, r7, #1
    mov r0, r0, lsl #24
    cmp r9, r0, asr #24
    mov r7, r0, asr #24
    bgt ov001_02202c9c_L88
ov001_02202c9c_Lc4:
    mov r0, r10, lsl #24
    mov r0, r0, asr #24
    bl native_fn_021fcd14
    add r0, r8, #1
    mov r0, r0, lsl #24
    mov r8, r0, asr #24
    cmp r8, #2
    blt ov001_02202c9c_L5c
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
