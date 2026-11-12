/* ov001 row 0x02214070: 236 bytes.
 *
 * What it does: 55 instructions; 6 call(s) to 0x021db8d0, 0x021f1c48, 0x021f1c68, +3 more; loops (back edge at +0x18); returns through pop {r3, pc}; 4 literal slot(s) in the extent
 *
 * Decoded shape: loop with 6 calls (55 instructions, 6 calls, 5 branches, 6 back edges, 4 literal slots).
 *
 *   pool +0xdc -> constant 0x02242aac (image word 0x02242aac)
 *   pool +0xe0 -> constant 0x02242ab4 (image word 0x02242ab4)
 *   pool +0xe4 -> constant 0x02242abd (image word 0x02242abd)
 *   pool +0xe8 -> constant 0x02242abc (image word 0x02242abc)
 *   branch +0x10 -> +0xa0
 *   branch +0x9c -> +0xd4
 *   branch +0xa4 -> +0xc4
 *   branch +0xb0 -> +0xd4
 *   branch +0xc0 -> +0xd4
 *   test +0x0c cmp r1, #0
 *   test +0x1c cmp r0, #0
 *   test +0xa0 cmp r1, #10
 *   test +0xac cmp r0, #0
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02214070; the literal pool and
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

extern void native_fn_021db8d0(void);
extern void native_fn_021f1c48(void);
extern void native_fn_021f1c68(void);
extern void native_fn_021f1bf0(void);
extern void native_fn_021f9248(void);
extern void native_fn_021f90b4(void);


asm u32 native_ov001_02214070 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr r0, =0x02242aac
    ldrsb r1, [r0, #2]
    cmp r1, #0
    bne ov001_02214070_La0
    ldr r0, [r0, #0x4]
    bl native_fn_021db8d0
    cmp r0, #0
    moveq r0, #1
    ldmeqia sp!, {r3, pc}
    ldr r1, =0x02242aac
    mov r0, #12
    ldrsb r2, [r1]
    ldr r1, =0x02242ab4
    smulbb r0, r2, r0
    ldr r0, [r1, r0]
    bl native_fn_021f1c48
    mov r0, #3
    bl native_fn_021f1c68
    ldr r1, =0x02242aac
    mov r0, #12
    ldrsb r2, [r1]
    ldr r1, =0x02242abd
    smulbb r0, r2, r0
    ldrsb r0, [r1, r0]
    bl native_fn_021f1bf0
    ldr r0, =0x02242aac
    mov r2, #12
    ldrsb r3, [r0]
    mov r0, #11
    mov r1, #0
    smulbb r12, r3, r2
    ldr r2, =0x02242abc
    mov r3, #2
    ldrb r2, [r2, r12]
    bl native_fn_021f9248
    ldr r0, =0x02242aac
    mov r1, #10
    strb r1, [r0, #0x2]
    b ov001_02214070_Ld4
ov001_02214070_La0:
    cmp r1, #10
    bne ov001_02214070_Lc4
    bl native_fn_021f90b4
    cmp r0, #0
    beq ov001_02214070_Ld4
    ldr r0, =0x02242aac
    mov r1, #100
    strb r1, [r0, #0x2]
    b ov001_02214070_Ld4
ov001_02214070_Lc4:
    mov r1, #0
    strb r1, [r0, #0x2]
    mov r0, #1
    ldmia sp!, {r3, pc}
ov001_02214070_Ld4:
    mov r0, #0
    ldmia sp!, {r3, pc}
}
