/* ov001 row 0x021fc2c0: 172 bytes.
 *
 * What it does: 41 instructions; 5 call(s) to 0x0202a634, 0x021fc390, 0x021fd1b8, +2 more; loops (back edge at +0x08); returns through pop {r4, r5, r6, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 5 calls (41 instructions, 5 calls, 9 branches, 2 back edges, 2 literal slots).
 *
 *   pool +0xa4 -> constant 0x02239c74 (image word 0x02239c74)
 *   pool +0xa8 -> constant 0x02239c10 (image word 0x02239c10)
 *   branch +0x20 -> +0x38
 *   branch +0x28 -> +0x48
 *   branch +0x30 -> +0x70
 *   branch +0x34 -> +0x8c
 *   branch +0x44 -> +0x8c
 *   branch +0x50 -> +0x8c
 *   branch +0x6c -> +0x8c
 *   branch +0x78 -> +0x80
 *   branch +0x90 -> +0x9c
 *   back edge +0x94 -> +0x00
 *   test +0x1c cmp r1, #0
 *   test +0x24 cmp r1, #1
 *   test +0x2c cmp r1, #2
 *   test +0x4c cmp r0, r6
 *   test +0x74 cmp r0, #2
 *   test +0x8c cmp r5, #0
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021fc2c0; the literal pool and
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

extern void native_fn_0202a634(void);
extern void native_fn_021fc390(void);
extern void native_fn_021fd1b8(void);
extern void native_fn_021fd288(void);


asm u32 native_ov001_021fc2c0 (register u32 a0)
{
ov001_021fc2c0_L0:
    stmdb sp!, {r4, r5, r6, lr}
    ldr r4, =0x02239c74
    bl native_fn_0202a634
    ldr r0, =0x02239c10
    mov r5, #0
    ldr r1, [r0, #0x68]
    ldr r6, [r0, #0x64]
    cmp r1, #0
    beq ov001_021fc2c0_L38
    cmp r1, #1
    beq ov001_021fc2c0_L48
    cmp r1, #2
    beq ov001_021fc2c0_L70
    b ov001_021fc2c0_L8c
ov001_021fc2c0_L38:
    bl native_fn_021fc390
    mov r0, #1
    str r0, [r4, #0x4]
    b ov001_021fc2c0_L8c
ov001_021fc2c0_L48:
    bl native_fn_021fd1b8
    cmp r0, r6
    beq ov001_021fc2c0_L8c
    ldr r2, [r4]
    mov r1, #2
    str r2, [r4, #0xc]
    str r1, [r4, #0x4]
    str r0, [r4, #0x8]
    mov r5, #1
    b ov001_021fc2c0_L8c
ov001_021fc2c0_L70:
    ldr r0, [r4, #0x8]
    cmp r0, #2
    beq ov001_021fc2c0_L80
    bl native_fn_021fd288
ov001_021fc2c0_L80:
    mov r0, #0
    ldr r6, [r4, #0x8]
    str r0, [r4, #0x4]
ov001_021fc2c0_L8c:
    cmp r5, #0
    beq ov001_021fc2c0_L9c
    bl ov001_021fc2c0_L0
    mov r6, r0
ov001_021fc2c0_L9c:
    mov r0, r6
    ldmia sp!, {r4, r5, r6, pc}
}
