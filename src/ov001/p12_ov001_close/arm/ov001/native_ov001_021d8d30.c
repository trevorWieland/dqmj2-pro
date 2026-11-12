/* ov001 row 0x021d8d30: 136 bytes.
 *
 * What it does: 31 instructions; 2 call(s) to 0x0202a8e0, 0x0202a954; loops (back edge at +0x34); returns through pop {r3, r4, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: loop with 2 calls (31 instructions, 2 calls, 2 branches, 3 back edges, 3 literal slots).
 *
 *   pool +0x7c -> native_data_0222d9a8 (image word 0x0222d9a8)
 *   pool +0x80 -> constant 0x02232b20 (image word 0x02232b20)
 *   pool +0x84 -> constant 0x02233178 (image word 0x02233178)
 *   back edge +0x34 -> +0x18
 *   branch +0x54 -> +0x70
 *   test +0x50 cmp r3, #904
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021d8d30; the literal pool and
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

extern u8 native_data_0222d9a8[];
extern void native_fn_0202a8e0(void);
extern void native_fn_0202a954(void);


asm u32 native_ov001_021d8d30 (register u32 a0)
{
    stmdb sp!, {r3, r4, lr}
    sub sp, sp, #20
    ldr r12, =native_data_0222d9a8
    add r3, sp, #4
    mov r4, #0
    mov r2, #7
ov001_021d8d30_L18:
    ldrb r1, [r12]
    ldrb r0, [r12, #0x1]
    add r12, r12, #2
    strb r1, [r3]
    strb r0, [r3, #0x1]
    add r3, r3, #2
    subs r2, r2, #1
    bne ov001_021d8d30_L18
    ldr r1, =0x02232b20
    mov r2, #0
    add r0, sp, #4
    str r2, [r1, #0x8]
    bl native_fn_0202a8e0
    mov r3, r0
    cmp r3, #904
    bhs ov001_021d8d30_L70
    ldr r2, =0x02233178
    mov r0, #0
    add r1, sp, #4
    str r0, [sp]
    bl native_fn_0202a954
    mov r4, r0
ov001_021d8d30_L70:
    mov r0, r4
    add sp, sp, #20
    ldmia sp!, {r3, r4, pc}
}
