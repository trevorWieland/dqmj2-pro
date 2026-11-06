#ifndef NATIVE_CARD_CALLBACK_TYPES_H
#define NATIVE_CARD_CALLBACK_TYPES_H
typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef struct CardTransfer { u32 count; const u8 *source; u8 *destination; u32 matched; } CardTransfer;
#define SPI_CONTROL (*(volatile u16 *)0x040001a0)
#define SPI_DATA (*(volatile u16 *)0x040001a2)
#endif
