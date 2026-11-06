#ifndef DQM_AES_TABLES_H
#define DQM_AES_TABLES_H
typedef unsigned int AesTableWord;
typedef char AesWordWidthMustBeFour[(sizeof(AesTableWord)==4)?1:-1];
typedef char AesWholeTableMustBe1024[(sizeof(AesTableWord[256])==1024)?1:-1];
extern const AesTableWord native_aes_Td2_022088b8[256];
extern const AesTableWord native_aes_Td3_02208cb8[256];
extern const AesTableWord native_aes_Td4_022090b8[256];
extern const AesTableWord native_aes_Te0_022094b8[256];
extern const AesTableWord native_aes_Te1_022098b8[256];
extern const AesTableWord native_aes_Te2_02209cb8[256];
extern const AesTableWord native_aes_Te3_0220a0b8[256];
extern const AesTableWord native_aes_Te4_0220a4b8[256];
extern const AesTableWord native_aes_Td0_0220a8b8[256];
extern const AesTableWord native_aes_Td1_0220acb8[256];
#endif
