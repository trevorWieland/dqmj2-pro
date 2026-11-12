/* ov001 row 0x021feba4: 120 bytes.
 *
 * What it does: 29 instructions; 3 call(s) to 0x0204b078, 0x0204afe0, 0x0204afe0; loops (back edge at +0x3c); returns through pop {r4, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 3 calls (29 instructions, 3 calls, 4 branches, 3 back edges, 1 literal slot).
 *
 *   pool +0x74 -> constant 0x02239c10 (image word 0x02239c10)
 *   branch +0x0c -> +0x20
 *   branch +0x14 -> +0x28
 *   branch +0x1c -> +0x2c
 *   branch +0x24 -> +0x2c
 *   test +0x04 cmp r0, #0
 *   test +0x10 cmp r0, #1
 *   test +0x18 cmp r0, #2
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021feba4; the literal pool and
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

extern void native_fn_0204b078(void);
extern void native_fn_0204afe0(void);


asm u32 native_ov001_021feba4 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    cmp r0, #0
    mov r4, #0
    beq ov001_021feba4_L20
    cmp r0, #1
    beq ov001_021feba4_L28
    cmp r0, #2
    b ov001_021feba4_L2c
ov001_021feba4_L20:
    mov r4, #4
    b ov001_021feba4_L2c
ov001_021feba4_L28:
    mov r4, #2
ov001_021feba4_L2c:
    ldr r0, =0x02239c10
    mov r2, r4
    ldr r0, [r0, #0x44]
    mov r1, #2
    bl native_fn_0204b078
    ldr r0, =0x02239c10
    mov r2, r4
    ldr r0, [r0, #0x44]
    mov r1, #1
    mov r3, #288
    bl native_fn_0204afe0
    ldr r0, =0x02239c10
    add r2, r4, #1
    ldr r0, [r0, #0x44]
    mov r1, #1
    mov r3, #384
    bl native_fn_0204afe0
    ldmia sp!, {r4, pc}
}
