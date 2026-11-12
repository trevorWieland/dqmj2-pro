/* ov001 row 0x02213844: 248 bytes.
 *
 * What it does: 59 instructions; 3 call(s) to 0x02041814, 0x02213844, 0x0204176c; loops (back edge at +0x8c); returns through pop {r3, r4, r5, r6, r7, r8, r9, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: block fill (59 instructions, 6 calls, 13 branches, 3 back edges, 3 literal slots).
 *
 *   pool +0xec -> constant 0x02242998 (image word 0x02242998)
 *   pool +0xf0 -> native_data_0222f1a4 (image word 0x0222f1a4)
 *   pool +0xf4 -> constant 0x0224299c (image word 0x0224299c)
 *   branch +0x30 -> +0xc8
 *   branch +0x34 -> +0x44
 *   branch +0x38 -> +0x60
 *   branch +0x3c -> +0x8c
 *   branch +0x40 -> +0xb8
 *   branch +0x4c -> +0x54
 *   branch +0x5c -> +0xc8
 *   branch +0x6c -> +0xc8
 *   branch +0x88 -> +0xc8
 *   branch +0x94 -> +0xc8
 *   branch +0xa0 -> +0xa8
 *   branch +0xb4 -> +0xc8
 *   branch +0xd4 -> +0xe0
 *   back edge +0xd8 -> +0x00
 *   test +0x24 cmp r8, #3
 *   test +0x48 cmp r0, #0
 *   test +0x68 cmp r0, r9
 *   test +0x90 cmp r0, #1
 *   test +0x9c cmp r0, #0
 *   test +0xc0 cmp r0, #2
 *   test +0xc8 cmp r6, #0
 *   test +0xd0 cmpne r8, r0
 *   1 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02213844; the literal pool and
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

extern u8 native_data_0222f1a4[];
extern void native_fn_02041814(void);
extern void native_fn_0204176c(void);


asm u32 native_ov001_02213844 (register u32 a0)
{
ov001_02213844_L0:
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, lr}
    ldr r1, =0x02242998
    ldr r2, =native_data_0222f1a4
    ldr r9, [r1, #0x4]
    mov r0, #12
    mla r7, r9, r0, r2
    ldr r8, [r1, #0x8]
    ldr r5, =0x0224299c
    mov r4, #2
    cmp r8, #3
    mov r6, #0
    addls pc, pc, r8, lsl #2
    b ov001_02213844_Lc8
    b ov001_02213844_L44
    b ov001_02213844_L60
    b ov001_02213844_L8c
    b ov001_02213844_Lb8
ov001_02213844_L44:
    ldr r0, [r7]
    cmp r0, #0
    beq ov001_02213844_L54
    blx r0
ov001_02213844_L54:
    mov r0, #1
    str r0, [r5, #0x4]
    b ov001_02213844_Lc8
ov001_02213844_L60:
    ldr r0, [r7, #0x4]
    blx r0
    cmp r0, r9
    beq ov001_02213844_Lc8
    ldr r2, [r5]
    mov r1, r4
    str r2, [r5, #0xc]
    str r1, [r5, #0x4]
    str r0, [r5, #0x8]
    mov r6, #1
    b ov001_02213844_Lc8
ov001_02213844_L8c:
    bl native_fn_02041814
    cmp r0, #1
    beq ov001_02213844_Lc8
    ldr r0, [r7, #0x8]
    cmp r0, #0
    beq ov001_02213844_La8
    blx r0
ov001_02213844_La8:
    mov r0, #3
    str r0, [r5, #0x4]
    mov r6, #1
    b ov001_02213844_Lc8
ov001_02213844_Lb8:
    ldr r0, [r5, #0x8]
    stmia r5, {r0, r6}
    cmp r0, #2
    moveq r4, r6
ov001_02213844_Lc8:
    cmp r6, #0
    ldrne r0, [r5, #0x4]
    cmpne r8, r0
    beq ov001_02213844_Le0
    bl ov001_02213844_L0
    mov r4, r0
ov001_02213844_Le0:
    bl native_fn_0204176c
    mov r0, r4
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
}
