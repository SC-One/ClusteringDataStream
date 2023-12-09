#ifndef SOCKETCLIENT_H
#define SOCKETCLIENT_H
#include <QObject>
#include <QWebSocket>
#include <Structures.h>

class SocketClient : public QObject {
  Q_OBJECT

public:
  explicit SocketClient(QUrl const &url = QUrl("ws://localhost:57777"),
                        QObject *parent = nullptr);

  void sendPoint(const QString &pointId, const Point &point);

signals:
  void clusterLabelsReceived(const ClusterLabel &data);

private slots:
  void onConnected();

  void onDisconnected();

  void onTextMessageReceived(const QString &message);

private:
  QWebSocket webSocket;
};

#endif // SOCKETCLIENT_H
