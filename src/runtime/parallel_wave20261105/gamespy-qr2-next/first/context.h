#include "types.h"
#include "records.h"
#ifndef _GT2_SOCKET_H_
#define _GT2_SOCKET_H_
GT2Result native_fn_020b59d4
(
	GT2Socket * socket,
	const char * localAddress,
	int outgoingBufferSize,
	int incomingBufferSize,
	gt2SocketErrorCallback callback,
	GTI2ProtocolType type
);
void gti2CloseSocket(GT2Socket socket);
void gti2Listen(GT2Socket socket, gt2ConnectAttemptCallback callback);
GT2Result gti2NewSocketConnection(GT2Socket socket, GT2Connection * connection, unsigned int ip, unsigned short port);
void native_fn_020b5cd0(GT2Connection connection);
GT2Connection native_fn_020b59ac(GT2Socket socket, unsigned int ip, unsigned short port);
GT2Bool gti2SocketSend(GT2Socket socket, unsigned int ip, unsigned short port, const GT2Byte * message, int len);
GT2Bool gti2SocketConnectionsThink(GT2Socket socket);
void gti2FreeClosedConnections(GT2Socket socket);
void gti2SocketError(GT2Socket socket);
#endif
#ifndef _GT2_CONNECTION_H_
#define _GT2_CONNECTION_H_
GT2Result gti2NewOutgoingConnection(GT2Socket socket, GT2Connection * connection, unsigned int ip, unsigned short port);
GT2Result gti2NewIncomingConnection(GT2Socket socket, GT2Connection * connection, unsigned int ip, unsigned short port);
GT2Result gti2StartConnectionAttempt
(
	GT2Connection connection,
	const GT2Byte * message,
	int len,
	GT2ConnectionCallbacks * callbacks
);
GT2Bool gti2AcceptConnection(GT2Connection connection, GT2ConnectionCallbacks * callbacks);
void gti2RejectConnection(GT2Connection connection, const GT2Byte * message, int len);
GT2Bool native_fn_020b4108(GT2Connection connection, const GT2Byte * message, int len);
GT2Bool gti2ConnectionThink(GT2Connection connection, gsi_time now);
void gti2CloseConnection(GT2Connection connection, GT2Bool hard);
void native_fn_020b42a4(GT2Connection connection);
void gti2ConnectionCleanup(GT2Connection connection);
#endif
#ifndef _GT2_BUFFER_H_
#define _GT2_BUFFER_H_
GT2Bool gti2AllocateBuffer(GTI2Buffer * buffer, int size);
int native_fn_020b3b50(const GTI2Buffer * buffer);
void native_fn_020b3b58(GTI2Buffer * buffer, GT2Byte b);
void native_fn_020b3b64(GTI2Buffer * buffer, unsigned short s);
void native_fn_020b3b80(GTI2Buffer * buffer, const GT2Byte * data, int len);
void gti2BufferShorten(GTI2Buffer * buffer, int start, int shortenBy);
#endif
#ifndef _GT2_CALLBACK_H_
#define _GT2_CALLBACK_H_
GT2Bool gti2SocketErrorCallback
(
	GT2Socket socket
);
GT2Bool gti2ConnectAttemptCallback
(
	GT2Socket socket,
	GT2Connection connection,
	unsigned int ip,
	unsigned short port,
	int latency,
	GT2Byte * message,
	int len
);
GT2Bool native_fn_020b3ca4
(
	GT2Connection connection,
	GT2Result result,
	GT2Byte * message,
	int len
);
GT2Bool gti2ReceivedCallback
(
	GT2Connection connection,
	GT2Byte * message,
	int len,
	GT2Bool reliable
);
GT2Bool native_fn_020b3d60
(
	GT2Connection connection,
	GT2CloseReason reason
);
GT2Bool gti2PingCallback
(
	GT2Connection connection,
	int latency
);
GT2Bool gti2SendFilterCallback
(
	GT2Connection connection,
	int filterID,
	const GT2Byte * message,
	int len,
	GT2Bool reliable
);
GT2Bool gti2ReceiveFilterCallback
(
	GT2Connection connection,
	int filterID,
	GT2Byte * message,
	int len,
	GT2Bool reliable
);
GT2Bool native_fn_020b3f00
(
	GT2Socket socket,
	GT2Connection connection,
	unsigned int ip,
	unsigned short port,
	GT2Bool reset,
	const GT2Byte * message,
	int len,
	GT2Bool send
);
GT2Bool gti2UnrecognizedMessageCallback
(
	GT2Socket socket,
	unsigned int ip,
	unsigned short port,
	GT2Byte * message,
	int len,
	GT2Bool * handled
);
#endif
#ifndef _GT2_MESSAGE_H_
#define _GT2_MESSAGE_H_
GT2Bool gti2ReceiveMessages(GT2Socket socket);
GT2Bool gti2Send(GT2Connection connection, const GT2Byte * message, int len, GT2Bool reliable);
GT2Bool gti2SendAppReliable(GT2Connection connection, const GT2Byte * message, int len);
GT2Bool gti2SendAppUnreliable(GT2Connection connection, const GT2Byte * message, int len);
GT2Bool gti2SendClientChallenge(GT2Connection connection, const char challenge[GTI2_CHALLENGE_LEN]);
GT2Bool gti2SendServerChallenge(GT2Connection connection, const char response[GTI2_RESPONSE_LEN], const char challenge[GTI2_CHALLENGE_LEN]);
GT2Bool gti2SendClientResponse(GT2Connection connection, const char response[GTI2_RESPONSE_LEN], const char * message, int len);
GT2Bool gti2SendAccept(GT2Connection connection);
GT2Bool gti2SendReject(GT2Connection connection, const GT2Byte * message, int len);
GT2Bool native_fn_020b5668(GT2Connection connection);
GT2Bool native_fn_020b56a8(GT2Connection connection);
GT2Bool native_fn_020b57a0(GT2Connection connection);
GT2Bool gti2SendNack(GT2Connection connection, unsigned short SNMin, unsigned short SNMax);
GT2Bool gti2SendPing(GT2Connection connection);
GT2Bool gti2SendPong(GT2Connection connection, GT2Byte * message, int len);
GT2Bool native_fn_020b589c(GT2Connection connection);
GT2Bool gti2SendClosedOnSocket(GT2Socket socket, unsigned int ip, unsigned short port);
GT2Bool native_fn_020b5900(GT2Connection connection, GTI2OutgoingBufferMessage * message);
GT2Bool gti2HandleConnectionReset(GT2Socket socket, unsigned int ip, unsigned short port);
GT2Bool gti2HandleHostUnreachable(GT2Socket socket, unsigned int ip, unsigned short port, GT2Bool send);
GT2Bool gti2WasMessageIDConfirmed(const GT2Connection connection, GT2MessageID messageID);
#endif
#ifndef _GT2_FILTER_H_
#define _GT2_FILTER_H_
GT2Bool gti2AddSendFilter(GT2Connection connection, gt2SendFilterCallback callback);
void gti2RemoveSendFilter(GT2Connection connection, gt2SendFilterCallback callback);
GT2Bool gti2FilteredSend(GT2Connection connection, int filterID, const GT2Byte * message, int len, GT2Bool reliable);
GT2Bool gti2AddReceiveFilter(GT2Connection connection, gt2ReceiveFilterCallback callback);
void gti2RemoveReceiveFilter(GT2Connection connection, gt2ReceiveFilterCallback callback);
GT2Bool gti2FilteredReceive(GT2Connection connection, int filterID, GT2Byte * message, int len, GT2Bool reliable);
#endif
#ifndef _GT2_UTILITY_H_
#define _GT2_UTILITY_H_
void gti2MessageCheck(const GT2Byte ** message, int * len);
#ifdef RECV_LOG
void gti2LogMessage
(
	unsigned int fromIP, unsigned short fromPort,
	unsigned int toIP, unsigned short toPort,
	const GT2Byte * message, int len
);
#endif
#endif

#undef GTI2_MAGIC_STRING
#define GTI2_MAGIC_STRING native_data_020e1714
extern const char native_data_020e1714[3];
