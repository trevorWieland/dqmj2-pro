/* ov006 row 0x021fc484: 88 bytes.
 *
 * What it does: Writes 3 blocks of 1 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x4c -> native_data2_0221c104 (image word 0x0221c104)
 *   pool +0x50 -> native_fn_021fc3a0+1 (image word 0x021fc3a1)
 *   pool +0x54 -> native_fn_021fc4dc+1 (image word 0x021fc4dd)
 *   branch +0x08 -> +0x10
 *   branch +0x0c -> +0x1e
 *   test +0x06 cmp r0, #0x1
 *   test +0x0a cmp r0, #0x4
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021fc484; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: three plausible C bodies were compiled first (word-copy loop, block-struct copy sized to the widest measured register list, and a guarded copy loop); none matched, the closest differs in 16 of 88 bytes. The meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_021f5740(void);
extern u8 native_data2_0221c104[];
extern void native_fn_021fc3a0(void);
extern void native_fn_021f52cc(void);
extern void native_fn_021ff718(void);
extern void native_fn_021ff6d4(void);
extern void native_fn_02200344(void);
extern void native_fn_021f23f4(void);
extern void native_fn_021fc4dc(void);


asm u32 native_ov006_021fc484 (register u32 a0)
{
    push {r3, lr}
    bl native_fn_021f5740
    cmp r0, #0x1
    beq ov006_021fc484_L10
    cmp r0, #0x4
    beq ov006_021fc484_L1e
    pop {r3, pc}
ov006_021fc484_L10:
    ldr r0, =native_data2_0221c104
    mov r1, #0x1
    strb r1, [r0, #0]
    ldr r0, =native_fn_021fc3a0+1
    bl native_fn_021f52cc
    pop {r3, pc}
ov006_021fc484_L1e:
    ldr r0, =native_data2_0221c104
    mov r1, #0x0
    strb r1, [r0, #0]
    bl native_fn_021ff718
    mov r0, #0x9
    bl native_fn_021ff6d4
    mov r1, #0x1
    mov r0, #0x0
    str r0, [sp]
    mov r0, #0xd
    add r2, r1, #0x0
    sub r3, r1, #0x2
    bl native_fn_02200344
    bl native_fn_021f23f4
    ldr r0, =native_fn_021fc4dc+1
    bl native_fn_021f52cc
    pop {r3, pc}
    mov r8, r8
}
