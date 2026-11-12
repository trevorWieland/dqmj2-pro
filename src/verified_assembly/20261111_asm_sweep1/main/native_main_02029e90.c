/* main row 0x02029e90: 96 bytes.
 *
 * What it does: Clears a 0xb4-byte block with ten four-register writeback stores and
 * primes the status words at +0x140..+0x148.
 *
 * Decoded shape: aggregate fill: 3 writeback block stores.
 *
 *   pool +0x58 -> native_data_020edd64 (image word 0x020edd64)
 *   pool +0x58 -> native_data_020edd64 (image word 0x020edd64)
 *   pool +0x5c -> native_data_020edd54 (image word 0x020edd54)
 *   block +0x1c: stm {r0, r1, r2, r3}
 *   block +0x20: stm {r0, r1, r2, r3}
 *   block +0x2c: stm {r0, r1, r2, r3}
 *   back edge +0x28 -> +0x1c
 *   memory +0x34 str r0, [lr]
 *   memory +0x40 str r2, [r1, #0x140]
 *   memory +0x44 ldr r2, [r0, #4]
 *   memory +0x4c str r2, [r1, #0x144]
 *   memory +0x50 str r0, [r1, #0x148]
 *   7 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x02029e90; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: the meaning of the fields, blocks and callee contracts
 * the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern u8 native_data_020edd54[];
extern u8 native_data_020edd64[];


asm u32 native_main_02029e90 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    mov r0, #0
    ldr lr, =native_data_020edd64
    mov r1, r0
    mov r2, r0
    mov r3, r0
    mov ip, #0xa
main_02029e90_L1c:
    stmia lr!, {r0, r1, r2, r3}
    stmia lr!, {r0, r1, r2, r3}
    subs ip, ip, #1
    bne main_02029e90_L1c
    stmia lr!, {r0, r1, r2, r3}
    ldr r1, =native_data_020edd64
    str r0, [lr]
    mov r2, #1
    ldr r0, =native_data_020edd54
    str r2, [r1, #0x140]
    ldr r2, [r0, #4]
    mov r0, #4
    str r2, [r1, #0x144]
    str r0, [r1, #0x148]
    ldmia sp!, {r3, pc}
}
