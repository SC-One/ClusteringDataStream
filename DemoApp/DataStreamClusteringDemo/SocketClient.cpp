#include "SocketClient.h"

#include <Parser.h>
#include <QThread>
#include <QWebSocket>

SocketClient::SocketClient(const QUrl &url, QObject *parent) : QObject(parent) {
  qDebug() << url;
  connect(&_webSocket, &QWebSocket::connected, this,
          &SocketClient::onConnected);
  connect(&_webSocket, &QWebSocket::disconnected, this,
          &SocketClient::onDisconnected);
  connect(&_webSocket, &QWebSocket::textMessageReceived, this,
          &SocketClient::onTextMessageReceived);
  connect(&_webSocket,
          QOverload<QAbstractSocket::SocketError>::of(&QWebSocket::error), this,
          [this](QAbstractSocket::SocketError error) {
            qDebug() << error << _webSocket.errorString();
          });

  _webSocket.open(url);
}

SocketClient::~SocketClient() {
  _webSocket.close(QWebSocketProtocol::CloseCodeNormal,
                   "See you later bro ^_*");
}

void SocketClient::sendPoint(const QString &pointId, const Point &point) {
  Message message;
  message.id = pointId;
  message.point = point;
  sendPoint(message);
}

void SocketClient::sendPoint(const Message &msg) {
  _webSocket.sendTextMessage(Parser::messageToJson(msg));
}

void SocketClient::onConnected() { qDebug() << "Connected to server."; }

void SocketClient::onDisconnected() { qDebug() << "Disconnected from server."; }

void SocketClient::onTextMessageReceived(const QString &message) {
  auto const clusterLabel = Parser::parseMessage(message);
  //  if (clusterLabel.cluster != 0) {
  //    qDebug() << message;
  //  }
  emit clusterLabelsReceived(clusterLabel);
}
