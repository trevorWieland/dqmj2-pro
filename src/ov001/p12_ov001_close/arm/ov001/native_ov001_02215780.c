/* ov001 row 0x02215780: 296 bytes.
 *
 * What it does: 71 instructions; 15 call(s) to 0x0203d294, 0x021db438, 0x021db8d0, +12 more; loops (back edge at +0x20); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: loop with 15 calls (71 instructions, 15 calls, 4 branches, 16 back edges, 3 literal slots).
 *
 *   pool +0x11c -> constant 0x02242ba0 (image word 0x02242ba0)
 *   pool +0x120 -> constant 0xffffd8f1 (image word 0xffffd8f1)
 *   pool +0x124 -> constant 0x0000270f (image word 0x0000270f)
 *   branch +0x10 -> +0x78
 *   back edge +0x3c -> +0x1c
 *   branch +0xa4 -> +0x10c
 *   branch +0xb4 -> +0xc4
 *   back edge +0x114 -> +0x8c
 *   test +0x0c cmp r0, #7
 *   test +0x38 cmp r0, #0
 *   test +0xa0 cmp r0, #0
 *   test +0xac cmp r0, #6
 *   test +0x110 cmp r8, #3
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02215780; the literal pool and
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

extern void native_fn_0203d294(void);
extern void native_fn_021db438(void);
extern void native_fn_021db8d0(void);
extern void native_fn_021db718(void);
extern void native_fn_021ee78c(void);
extern void native_fn_022024d4(void);
extern void native_fn_02215760(void);
extern void native_fn_021dbd24(void);
extern void native_fn_021d9494(void);


asm u32 native_ov001_02215780 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    ldr r4, =0x02242ba0
    ldrb r0, [r4, #0x2]
    cmp r0, #7
    bne ov001_02215780_L78
    mov r6, #3
    mov r5, #0
ov001_02215780_L1c:
    mov r0, r6
    bl native_fn_0203d294
    mov r1, r0
    mov r0, r5
    bl native_fn_021db438
    mov r4, r0
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_02215780_L1c
    ldr r1, =0xffffd8f1
    mov r0, r4
    bl native_fn_021db718
    mov r3, #1
    ldr r1, =0x0000270f
    mov r0, r4
    str r3, [sp]
    sub r2, r3, #2
    bl native_fn_021ee78c
    ldrb r0, [r4, #0x31e]
    ldrb r1, [r4, #0x31f]
    ldr r2, =0x0000270f
    bl native_fn_022024d4
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
ov001_02215780_L78:
    ldr r7, =0x0000270f
    mov r8, #0
    mov r6, #4
    mov r11, #1
    mvn r5, #0
ov001_02215780_L8c:
    bl native_fn_02215760
    mov r1, r8
    bl native_fn_021db438
    mov r9, r0
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_02215780_L10c
    ldrb r0, [r4, #0x2]
    cmp r0, #6
    moveq r10, r7
    beq ov001_02215780_Lc4
    mov r0, r9
    bl native_fn_021dbd24
    sub r10, r0, #1
ov001_02215780_Lc4:
    mov r0, r9
    mov r1, r6
    mov r2, r11
    bl native_fn_021d9494
    mov r0, r9
    rsb r1, r10, #0
    bl native_fn_021db718
    mov r0, #1
    str r0, [sp]
    mov r0, r9
    mov r1, r10
    mov r2, r5
    mov r3, #1
    bl native_fn_021ee78c
    ldrb r0, [r9, #0x31e]
    ldrb r1, [r9, #0x31f]
    mov r2, r10
    bl native_fn_022024d4
ov001_02215780_L10c:
    add r8, r8, #1
    cmp r8, #3
    blt ov001_02215780_L8c
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
