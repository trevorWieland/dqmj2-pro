/* ov006 row 0x021f4014: 536 bytes.
 *
 * What it does: Writes one block of 2 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x1f8 -> native_data_0220b430 (image word 0x0220b430)
 *   pool +0x1fc -> native_data_0221c060 (image word 0x0221c060)
 *   pool +0x200 -> constant 0xc1fffcff (image word 0xc1fffcff)
 *   pool +0x204 -> constant 0xfffff3ff (image word 0xfffff3ff)
 *   pool +0x208 -> native_data_0220b41c (image word 0x0220b41c)
 *   pool +0x20c -> native_data_0220b420 (image word 0x0220b420)
 *   pool +0x210 -> native_data_0220b468 (image word 0x0220b468)
 *   pool +0x214 -> native_fn_021f42a4+1 (image word 0x021f42a5)
 *   back edge +0x8c -> +0x54
 *   back edge +0xd4 -> +0x96
 *   back edge +0x11a -> +0xde
 *   back edge +0x180 -> +0x14e
 *   back edge +0x1a4 -> +0x128
 *   test +0x8a cmp r6, #0xa
 *   test +0xd2 cmp r6, #0x2
 *   test +0x118 cmp r6, #0x2
 *   test +0x17e cmp r4, #0x3
 *   test +0x1a2 cmp r0, #0x4
 *   37 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f4014; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: the meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern u8 native_data_0220b430[];
extern void ov006_clear_buffer_02203c08(void);
extern u8 native_data9_0221c060[];
extern void native_fn_0220303c(void);
extern u8 native_data_0220b41c[];
extern u8 native_data_0220b420[];
extern void native_fn_02203058(void);
extern void native_fn_02202dcc(void);
extern void native_fn_02202f54(void);
extern void native_fn_0220342c(void);
extern u8 native_data_0220b468[];
extern void native_fn_022037c0(void);
extern void native_fn_02202c5c(void);
extern void native_fn_021f42a4(void);
extern void native_fn_0220490c(void);
extern void native_fn_021f4944(void);


asm u32 native_ov006_021f4014 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    sub sp, #0x28
    ldr r1, =native_data_0220b430
    add r0, sp, #0x18
    ldrh r2, [r1, #0x20]
    strh r2, [r0, #0x8]
    ldrh r2, [r1, #0x22]
    strh r2, [r0, #0xa]
    ldrh r2, [r1, #0x24]
    ldrh r1, [r1, #0x26]
    strh r2, [r0, #0xc]
    strh r1, [r0, #0xe]
    mov r1, #0x1c
    strh r1, [r0, #0xc]
    mov r1, #0x14
    strh r1, [r0, #0xe]
    mov r0, #0x6c
    mov r1, #0x4
    bl ov006_clear_buffer_02203c08
    ldr r4, =native_data9_0221c060
    mov r6, #0x0
    str r0, [r4, #0]
    mov r1, #0x1f
    add r0, #0x60
    strb r1, [r0, #0]
    ldr r0, [r4, #0]
    mov r7, #0x3
    add r0, #0x63
    strb r6, [r0, #0]
    ldr r0, [r4, #0]
    mov r1, #0x1
    add r0, #0x66
    strb r1, [r0, #0]
    ldr r0, [r4, #0]
    add r5, r6, #0x0
    add r0, #0x67
    strb r1, [r0, #0]
    ldr r0, [r4, #0]
    lsl r7, r7, #0xa
    add r0, #0x68
    strb r1, [r0, #0]
ov006_021f4014_L54:
    mov r0, #0x0
    mov r1, #0x36
    bl native_fn_0220303c
    ldr r1, [r4, #0]
    add r6, r6, #0x1
    add r1, r1, r5
    str r0, [r1, #0x10]
    ldr r0, [r4, #0]
    ldr r1, =0xc1fffcff
    add r0, r0, r5
    ldr r0, [r0, #0x10]
    ldr r2, [r0, #0]
    and r2, r1
    mov r1, #0x2
    lsl r1, r1, #0x8
    orr r1, r2
    str r1, [r0, #0]
    ldr r0, [r4, #0]
    ldr r1, =0xfffff3ff
    add r0, r0, r5
    ldr r0, [r0, #0x10]
    add r5, r5, #0x4
    ldrh r2, [r0, #0x4]
    and r1, r2
    orr r1, r7
    strh r1, [r0, #0x4]
    cmp r6, #0xa
    blt ov006_021f4014_L54
    mov r6, #0x0
    ldr r4, =native_data_0220b41c
    ldr r7, =native_data9_0221c060
    add r5, r6, #0x0
ov006_021f4014_L96:
    ldrb r1, [r4, #0]
    mov r0, #0x0
    bl native_fn_0220303c
    ldr r1, [r7, #0]
    add r6, r6, #0x1
    add r1, r1, r5
    str r0, [r1, #0x38]
    ldr r0, [r7, #0]
    ldr r1, =0xc1fffcff
    add r0, r0, r5
    ldr r0, [r0, #0x38]
    add r4, r4, #0x1
    ldr r2, [r0, #0]
    and r2, r1
    mov r1, #0x2
    lsl r1, r1, #0x8
    orr r1, r2
    str r1, [r0, #0]
    ldr r0, [r7, #0]
    ldr r1, =0xfffff3ff
    add r0, r0, r5
    ldr r0, [r0, #0x38]
    add r5, r5, #0x4
    ldrh r2, [r0, #0x4]
    and r2, r1
    mov r1, #0x3
    lsl r1, r1, #0xa
    orr r1, r2
    strh r1, [r0, #0x4]
    cmp r6, #0x2
    blt ov006_021f4014_L96
    mov r6, #0x0
    ldr r4, =native_data_0220b420
    ldr r7, =native_data9_0221c060
    add r5, r6, #0x0
ov006_021f4014_Lde:
    ldrb r1, [r4, #0]
    mov r0, #0x0
    mov r2, #0x1
    bl native_fn_02203058
    ldr r1, [r7, #0]
    mov r2, #0x2
    add r1, r1, r5
    str r0, [r1, #0x40]
    ldr r0, [r7, #0]
    mov r1, #0x0
    add r0, r0, r5
    ldr r0, [r0, #0x40]
    mvn r1, r1
    lsl r2, r2, #0x8
    mov r3, #0x0
    bl native_fn_02202dcc
    ldr r0, [r7, #0]
    mov r1, #0x0
    add r0, r0, r5
    ldr r0, [r0, #0x40]
    mvn r1, r1
    mov r2, #0x3
    bl native_fn_02202f54
    add r6, r6, #0x1
    add r4, r4, #0x1
    add r5, r5, #0x4
    cmp r6, #0x2
    blt ov006_021f4014_Lde
    mov r0, #0x0
    add r1, sp, #0x18
    str r0, [sp, #0x10]
    strh r0, [r1, #0x2]
    add r7, r0, #0x0
    str r0, [sp, #0x14]
ov006_021f4014_L128:
    add r0, sp, #0x1c
    str r0, [sp, #0]
    mov r0, #0x0
    mov r1, #0xc
    mov r2, #0x4
    add r3, r0, #0x0
    str r0, [sp, #0x4]
    bl native_fn_0220342c
    ldr r1, =native_data9_0221c060
    mov r4, #0x0
    ldr r1, [r1, #0]
    add r6, sp, #0x18
    str r0, [r1, r7]
    ldr r0, [sp, #0x14]
    ldr r1, =native_data_0220b468
    lsl r0, r0, #0x1
    strh r4, [r6, #0x8]
    add r5, r1, r0
ov006_021f4014_L14e:
    ldrh r0, [r5, #0]
    strh r0, [r6, #0]
    ldrh r0, [r6, #0xe]
    str r0, [sp, #0]
    mov r0, #0x2
    str r0, [sp, #0x4]
    mov r0, #0x12
    lsl r0, r0, #0x6
    str r0, [sp, #0x8]
    add r0, sp, #0x18
    str r0, [sp, #0xc]
    ldr r0, =native_data9_0221c060
    ldrh r1, [r6, #0x8]
    ldr r0, [r0, #0]
    ldrh r2, [r6, #0xa]
    ldrh r3, [r6, #0xc]
    ldr r0, [r7, r0]
    bl native_fn_022037c0
    ldrh r0, [r6, #0x8]
    add r4, r4, #0x1
    add r5, r5, #0x2
    add r0, #0x20
    strh r0, [r6, #0x8]
    cmp r4, #0x3
    blt ov006_021f4014_L14e
    mov r0, #0x0
    ldr r1, [sp, #0x1c]
    add r2, r0, #0x0
    bl native_fn_02202c5c
    ldr r1, =native_data9_0221c060
    ldr r1, [r1, #0]
    add r1, r1, r7
    str r0, [r1, #0x48]
    ldr r0, [sp, #0x14]
    add r7, r7, #0x4
    add r0, r0, #0x3
    str r0, [sp, #0x14]
    ldr r0, [sp, #0x10]
    add r0, r0, #0x1
    str r0, [sp, #0x10]
    cmp r0, #0x4
    blt ov006_021f4014_L128
    mov r0, #0x0
    mov r1, #0x44
    mov r2, #0x1
    bl native_fn_02203058
    ldr r1, =native_data9_0221c060
    mov r3, #0x0
    ldr r2, [r1, #0]
    str r0, [r2, #0x58]
    ldr r0, [r1, #0]
    mov r1, #0x0
    mov r2, #0x2
    ldr r0, [r0, #0x58]
    mvn r1, r1
    lsl r2, r2, #0x8
    bl native_fn_02202dcc
    ldr r0, =native_data9_0221c060
    mov r1, #0x0
    ldr r0, [r0, #0]
    mvn r1, r1
    ldr r0, [r0, #0x58]
    mov r2, #0x2
    bl native_fn_02202f54
    mov r0, #0x0
    ldr r1, =native_fn_021f42a4+1
    add r2, r0, #0x0
    mov r3, #0x78
    bl native_fn_0220490c
    ldr r1, =native_data9_0221c060
    ldr r1, [r1, #0]
    str r0, [r1, #0x5c]
    mov r0, #0x0
    mov r1, #0xc0
    bl native_fn_021f4944
    add sp, #0x28
    pop {r3, r4, r5, r6, r7, pc}
    mov r8, r8
}
