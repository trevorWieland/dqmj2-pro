/* ov001 row 0x022065f0: 192 bytes.
 *
 * What it does: 48 instructions; 8 call(s) to 0x020630b0, 0x0205f98c, 0x02206668, +5 more; loops (back edge at +0x18); returns through pop {r4, r5, r6, r7, r8, pc}
 *
 * Decoded shape: loop with 8 calls (48 instructions, 8 calls, 3 branches, 7 back edges, 0 literal slots).
 *
 *   branch +0x28 -> +0x90
 *   branch +0x54 -> +0x7c
 *   branch +0x68 -> +0x78
 *   back edge +0x88 -> +0x34
 *   back edge +0xb8 -> +0x94
 *   test +0x24 cmp r1, r0
 *   test +0x48 cmp r6, #0
 *   test +0x58 cmp r6, #4
 *   test +0x84 cmp r5, #20
 *   test +0xb4 cmp r5, #20
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x022065f0; the literal pool and
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

extern void native_fn_020630b0(void);
extern void native_fn_0205f98c(void);
extern void native_fn_022023a8(void);


asm u32 native_ov001_022065f0 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    mov r7, r0
    ldr r0, [r7, #0x28]
    mov r6, r1
    ldr r0, [r0, #0x1e8]
    ldrb r0, [r0, #0xab]
    bl native_fn_020630b0
    ldr r1, [r7, #0x38]
    mov r5, #0
    cmp r1, r0
    bge ov001_022065f0_L90
    mov r8, r5
    mov r4, #160
ov001_022065f0_L34:
    add r1, r5, #1
    ldr r0, [r7, #0x1c]
    and r1, r1, #255
    bl native_fn_0205f98c
    ldr r1, [r0, #0x7c]
    cmp r6, #0
    bic r1, r1, #2
    str r1, [r0, #0x7c]
    beq ov001_022065f0_L7c
    cmp r6, #4
    rsblo r1, r6, #164
    movlo r6, r8
    andlo r1, r1, #255
    blo ov001_022065f0_L78
    sub r2, r6, #4
    mov r1, r4
    and r6, r2, #255
ov001_022065f0_L78:
    bl native_fn_022023a8
ov001_022065f0_L7c:
    add r0, r5, #1
    and r5, r0, #255
    cmp r5, #20
    blo ov001_022065f0_L34
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
ov001_022065f0_L90:
    mov r4, #188
ov001_022065f0_L94:
    add r1, r5, #1
    ldr r0, [r7, #0x1c]
    and r1, r1, #255
    bl native_fn_0205f98c
    mov r1, r4
    bl native_fn_022023a8
    add r0, r5, #1
    and r5, r0, #255
    cmp r5, #20
    blo ov001_022065f0_L94
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
