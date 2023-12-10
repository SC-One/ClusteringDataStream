#include "DenStreamClusterer.h"
#include <QColor>
#include <SocketClient.h>
#include <chrono>

DenStreamClusterer::DenStreamClusterer(QObject *parent)
    : QObject{parent}, _continueSending(true) {
  _client.reset(new SocketClient);
  connect(_client.get(), &SocketClient::clusterLabelsReceived, this,
          [this](const ClusterLabel &data) {
            emit clusterLabelForId(data.id, data.cluster);
          });
  connect(
      this, &DenStreamClusterer::newDataShouldSend, this,
      [this](const Message &data) { _client->sendPoint(data); },
      Qt::QueuedConnection);

  _consumerThread.reset(new std::thread([this]() {
    Message data; // tmp stage
    while (_continueSending) {
      if (_pointsQueuee.dequeue(data)) {
        emit newDataShouldSend(data);
      } else {
        if (_pointsQueuee.isEmpty()) {
          std::this_thread::sleep_for(std::chrono::milliseconds(177));
        }
      }
    }
  }));
}

DenStreamClusterer::~DenStreamClusterer() {
  _continueSending = false;
  if (_consumerThread->joinable()) {
    _consumerThread->join();
  }
}

void DenStreamClusterer::addPoint(const QString &id, double latitude,
                                  double longitude) {
  Message msg;
  msg.id = id;
  msg.point.x = latitude;
  msg.point.y = longitude;
  _pointsQueuee.enqueue(msg);
}

QString DenStreamClusterer::getColor(int clusterNumber) {
  return QColor(static_cast<Qt::GlobalColor>(clusterNumber + 4))
      .name(); // bypass first 4 colors
}
