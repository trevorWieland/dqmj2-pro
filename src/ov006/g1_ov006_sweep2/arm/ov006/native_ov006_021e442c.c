/* ov006 row 0x021e442c: 64 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x38 -> constant 0x02218d24 (image word 0x02218d24)
 *   pool +0x3c -> native_data_02207d18 (image word 0x02207d18)
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021e442c; the literal pool and
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

extern void ov006_noop_021e3cd4(void);
extern void native_fn_020644f4(void);
extern void native_fn_021e7d98(void);
extern u8 native_data_02207d18[];
extern void ov006_commit_mode_transition_021e9148(void);


asm u32 native_ov006_021e442c (register u32 a0)
{
    stmdb sp!, {r3, lr}
    bl ov006_noop_021e3cd4
    mov r0, #1
    bl native_fn_020644f4
    mov r0, #0
    bl native_fn_021e7d98
    ldr r2, =0x02218d24
    mov r1, #0
    ldr r0, =native_data_02207d18
    str r1, [r2, #0x4]
    mov r3, #1
    str r3, [r2]
    bl ov006_commit_mode_transition_021e9148
    ldmia sp!, {r3, pc}
}
