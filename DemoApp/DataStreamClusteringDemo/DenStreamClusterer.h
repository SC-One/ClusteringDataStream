#ifndef DENSTREAMCLUSTERER_H
#define DENSTREAMCLUSTERER_H

#include <QObject>
#include <QScopedPointer>
#include <QThread>
#include <Structures.h>
#include <ThreadSafeQueue.h>
#include <thread>

class SocketClient;
class DenStreamClusterer : public QObject {
  Q_OBJECT
public:
  explicit DenStreamClusterer(QObject *parent = nullptr);
  ~DenStreamClusterer();
  // thread safe
  Q_INVOKABLE void addPoint(QString const &id, double latitude,
                            double longitude);
signals:
  void clusterLabelForId(QString const &id, int cluster);

  void newDataShouldSend(const Message &data);

private:
  ThreadSafeQueue<Message> _pointsQueuee;
  bool _continueSending;
  QScopedPointer<std::thread> _consumerThread;

  QScopedPointer<SocketClient> _client;
};

#endif // DENSTREAMCLUSTERER_H
