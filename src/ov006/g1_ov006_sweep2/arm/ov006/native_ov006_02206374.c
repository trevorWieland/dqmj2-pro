/* ov006 row 0x02206374: 116 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   back edge +0x6c -> +0x1c
 *   test +0x68 cmp r6, #12
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x02206374; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity proves the instruction stream, not the meaning of the fields, blocks and callee contracts it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_0206cc70(void);
extern void native_fn_021e7f08(void);


asm u32 native_ov006_02206374 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    mov r0, #1
    bl native_fn_0206cc70
    mov r7, #40
    mov r6, #0
    mov r5, #12
    mov r4, r7
ov006_02206374_L1c:
    mov r1, r6, lsr #31
    mov r2, r6, asr #1
    rsb r0, r1, r6, lsl #30
    add r2, r6, r2, lsr #30
    add r1, r1, r0, ror #30
    mov r0, r2, asr #2
    mul r2, r1, r7
    add r0, r0, #1
    mul r3, r0, r4
    add r1, r2, #48
    mov r0, r1, asr #2
    mov r2, r3, asr #2
    add r1, r1, r0, lsr #29
    add r2, r3, r2, lsr #29
    mov r0, r5
    mov r1, r1, asr #3
    mov r2, r2, asr #3
    bl native_fn_021e7f08
    add r6, r6, #1
    cmp r6, #12
    blt ov006_02206374_L1c
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
