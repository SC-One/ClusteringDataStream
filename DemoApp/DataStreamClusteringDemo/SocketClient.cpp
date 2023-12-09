#include "SocketClient.h"

#include <Parser.h>
#include <QWebSocket>

SocketClient::SocketClient(const QUrl &url, QObject *parent) : QObject(parent) {
  connect(&webSocket, &QWebSocket::connected, this, &SocketClient::onConnected);
  connect(&webSocket, &QWebSocket::disconnected, this,
          &SocketClient::onDisconnected);
  connect(&webSocket, &QWebSocket::textMessageReceived, this,
          &SocketClient::onTextMessageReceived);

  webSocket.open(url);
}

void SocketClient::sendPoint(const QString &pointId, const Point &point) {
  Message message;
  message.id = pointId;
  message.point = point;

  webSocket.sendTextMessage(Parser::messageToJson(message));
}

void SocketClient::onConnected() { qDebug() << "Connected to server."; }

void SocketClient::onDisconnected() { qDebug() << "Disconnected from server."; }

void SocketClient::onTextMessageReceived(const QString &message) {
  auto const clusterLabel = Parser::parseMessage(message);
  emit clusterLabelsReceived(clusterLabel);
}
