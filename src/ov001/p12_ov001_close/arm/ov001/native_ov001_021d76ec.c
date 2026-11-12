/* ov001 row 0x021d76ec: 96 bytes.
 *
 * What it does: 22 instructions; 1 call(s) to 0x020448d8; loops (back edge at +0x48); returns through pop {r3, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 1 call (22 instructions, 1 call, 3 branches, 1 back edge, 2 literal slots).
 *
 *   pool +0x58 -> constant 0x0222fd50 (image word 0x0222fd50)
 *   pool +0x5c -> constant 0x0222fda0 (image word 0x0222fda0)
 *   branch +0x18 -> +0x50
 *   branch +0x34 -> +0x50
 *   branch +0x40 -> +0x50
 *   test +0x08 cmp r0, r12
 *   test +0x14 cmp r0, #49
 *   test +0x30 cmp r0, #0
 *   test +0x3c cmp r0, #2
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021d76ec; the literal pool and
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

extern void native_fn_020448d8(void);


asm u32 native_ov001_021d76ec (register u32 a0)
{
    stmdb sp!, {r3, lr}
    mvn r12, #0
    cmp r0, r12
    ldreq r0, =0x0222fd50
    ldreqsh r0, [r0, #76]
    cmp r0, #49
    bge ov001_021d76ec_L50
    mov r2, #120
    mul r2, r0, r2
    ldr r3, =0x0222fda0
    ldrb r0, [r3, r2]
    add r2, r3, r2
    cmp r0, #0
    beq ov001_021d76ec_L50
    ldrb r0, [r2, #0x1]
    cmp r0, #2
    bne ov001_021d76ec_L50
    add r0, r2, #28
    bl native_fn_020448d8
    mov r12, r0
ov001_021d76ec_L50:
    mov r0, r12
    ldmia sp!, {r3, pc}
}
