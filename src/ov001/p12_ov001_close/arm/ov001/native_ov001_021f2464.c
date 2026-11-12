/* ov001 row 0x021f2464: 116 bytes.
 *
 * What it does: 27 instructions; 1 call(s) to 0x0207b004; loops (back edge at +0x40); returns through pop {r4, r5, r6, r7, r8, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 1 call (27 instructions, 1 call, 3 branches, 2 back edges, 2 literal slots).
 *
 *   pool +0x6c -> constant 0x0223989c (image word 0x0223989c)
 *   pool +0x70 -> native_data_0222dfd8 (image word 0x0222dfd8)
 *   branch +0x14 -> +0x64
 *   branch +0x34 -> +0x50
 *   back edge +0x60 -> +0x28
 *   test +0x10 cmp r0, #0
 *   test +0x30 cmp r6, r0
 *   test +0x44 cmp r0, #0
 *   test +0x5c cmp r0, r7
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021f2464; the literal pool and
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

extern u8 native_data_0222dfd8[];
extern void native_fn_0207b004(void);


asm u32 native_ov001_021f2464 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    ldr r1, =0x0223989c
    mov r6, r0
    ldrb r0, [r1, #0x10]
    cmp r0, #0
    beq ov001_021f2464_L64
    ldr r4, =native_data_0222dfd8
    mov r5, #0
    mov r8, #16777216
    mvn r7, #0
ov001_021f2464_L28:
    mov r0, r5, lsl #1
    ldrsh r0, [r4, r0]
    cmp r6, r0
    bne ov001_021f2464_L50
    mov r0, r6
    mov r1, r8
    bl native_fn_0207b004
    cmp r0, #0
    movne r0, #0
    ldmneia sp!, {r4, r5, r6, r7, r8, pc}
ov001_021f2464_L50:
    add r5, r5, #1
    mov r0, r5, lsl #1
    ldrsh r0, [r4, r0]
    cmp r0, r7
    bne ov001_021f2464_L28
ov001_021f2464_L64:
    mov r0, #1
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
