#ifndef SOCKETCLIENT_H
#define SOCKETCLIENT_H
#include <QObject>
#include <QWebSocket>
#include <Structures.h>

class SocketClient : public QObject {
  Q_OBJECT

public:
  explicit SocketClient(
      QUrl const &url =
          QUrl("ws://localhost:57777/?epsilonParam=0.67&batchSizeProcess=5"),
      QObject *parent = nullptr);
  ~SocketClient();

  void sendPoint(const QString &pointId, const Point &point);
  void sendPoint(Message const &msg);

signals:
  void clusterLabelsReceived(const ClusterLabel &data);

private slots:
  void onConnected();

  void onDisconnected();

  void onTextMessageReceived(const QString &message);

private:
  QWebSocket _webSocket;
};

#endif // SOCKETCLIENT_H
