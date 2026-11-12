/* ov001 row 0x021d8f08: 128 bytes.
 *
 * What it does: 30 instructions; 2 call(s) to 0x0202a8e0, 0x0202a954; loops (back edge at +0x34); returns through pop {r4, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 2 calls (30 instructions, 2 calls, 2 branches, 3 back edges, 2 literal slots).
 *
 *   pool +0x78 -> native_data_0222d9c4 (image word 0x0222d9c4)
 *   pool +0x7c -> constant 0x02232c20 (image word 0x02232c20)
 *   back edge +0x34 -> +0x18
 *   branch +0x50 -> +0x6c
 *   test +0x4c cmp r3, #960
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021d8f08; the literal pool and
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

extern u8 native_data_0222d9c4[];
extern void native_fn_0202a8e0(void);
extern void native_fn_0202a954(void);


asm u32 native_ov001_021d8f08 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    sub sp, sp, #24
    ldr r12, =native_data_0222d9c4
    add r3, sp, #4
    mov r4, #0
    mov r2, #9
ov001_021d8f08_L18:
    ldrb r1, [r12]
    ldrb r0, [r12, #0x1]
    add r12, r12, #2
    strb r1, [r3]
    strb r0, [r3, #0x1]
    add r3, r3, #2
    subs r2, r2, #1
    bne ov001_021d8f08_L18
    ldrb r1, [r12]
    add r0, sp, #4
    strb r1, [r3]
    bl native_fn_0202a8e0
    mov r3, r0
    cmp r3, #960
    bhs ov001_021d8f08_L6c
    ldr r2, =0x02232c20
    mov r0, #0
    add r1, sp, #4
    str r0, [sp]
    bl native_fn_0202a954
    mov r4, r0
ov001_021d8f08_L6c:
    mov r0, r4
    add sp, sp, #24
    ldmia sp!, {r4, pc}
}
